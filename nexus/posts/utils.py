import datetime
import time
import praw    
import re, random
from string import punctuation

from django.utils.timezone import utc

from django.utils.timezone import utc
from django.shortcuts import get_object_or_404

from posts.models import Post
from posts.forms import PostForm
from hubs.models import Hub
from profiles.models import User




def rank_hot(stories, top=180, consider=1000):
    # top - number of stories to show,
    # consider - number of latest stories to rank
    
    def score(post, gravity=1.2, timebase=120):
        # number_of_comments = len(post.comments.all())
        rating = (post.score + 1)**0.8 # + number_of_comments
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        age = int((now - post.pub_date).total_seconds())/60
        # temporary hack to not let score be below zero
        try:
            if float(rating) > 1:
                scr = rating/(age+timebase)**gravity
            else:
                scr = 0
        except:
            scr = 0
        return scr

    latest_stories = stories.order_by('-pub_date')#[:consider]
    #comprehension, stories with rating, sorted
    stories_with_rating = [(score(story), story) for story in latest_stories]
    #ranked_stories = sorted(stories_with_rating, reverse = True) - old but worked
    ranked_stories = sorted(latest_stories, key=score, reverse = True)
    #strip away the rating and return only stories
    # return [story for _, story in ranked_stories][:top] - old but worked
    return ranked_stories

def rank_top(stories, timespan = None):
    # if timespan == "day":
    #     day = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('day')
    #     stories = stories.filter(pub_date__day = day)        
    # elif timespan == "month":
    #     month = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('month')
    #     stories = stories.filter(pub_date__month = month)        
    # elif timespan == "all-time":
    #     year = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('year')
    #     stories = stories.filter(pub_date__year = year)                
    
    top_stories = stories.order_by('-score')
    return top_stories









def check_if_rational(request):
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io":
        rational = True
    return rational

def check_if_fictionhub(request):
    fictionhub = False
    if request.META['HTTP_HOST'] == "fictionhub.io":
        fictionhub = True
    return fictionhub



def check_if_daily(request):
    daily = False
    #        request.META['HTTP_HOST'] == "localhost:8000" or \
    if request.META['HTTP_HOST'] == "daily.fictionhub.io" or \
       request.META['HTTP_HOST'] == "writingstreak.io" or \
       request.META['HTTP_HOST'] == "streak.fictionhub.io":
        daily = True
    return daily






def age(timestamp):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    # usage: age(prompt.created_utc)
    return age_in_minutes





from django.template.defaultfilters import slugify



def count_words(post):
    r = re.compile(r'[{}]'.format(punctuation))
    wordcount = 0
    text = r.sub(' ', post.body)
    wordcount += len(text.split())

    if post.children:
        for child in post.children.all():
            text = r.sub(' ',child.body)
            wordcount += len(text.split())
    if wordcount > 1000:
        wordcount = str(int(wordcount/1000)) + "K"

    return wordcount



def get_reply_list(replies=None, rankby="hot"):
    """Recursively build a list of comments."""
    yield 'in'

    # Loop through all the comments I've passed
    for reply in replies:
        # Add comment to the list
        yield reply
        # get comment's children
        children = reply.children.all()
        if rankby == "hot":
            ranked_children = rank_hot(children, top=32)
        elif rankby == "top":
            ranked_children = rank_top(children, timespan = "all-time")
        elif rankby == "new":
            ranked_children = children.order_by('-pub_date')
        else:
            ranked_children = []
        
        # If there's any children
        if len(ranked_children):
            reply.leaf=False
            # loop through children, and apply this function
            for x in get_reply_list(ranked_children, rankby=rankby):
                yield x
        else:
            reply.leaf=True
    yield 'out'



def get_replies(post, rankby="new",comment_id=None):
    top_lvl_replies = Post.objects.filter(parent = post)

    # Rank comments
    if rankby == "hot":
        ranked_comments = rank_hot(top_lvl_replies, top=32)
    elif rankby == "top":
        ranked_comments = rank_top(top_lvl_replies, timespan = "all-time")
    elif rankby == "new":
        ranked_comments = top_lvl_replies.order_by('-pub_date')
    else:
        ranked_comments = []

    # Permalink to one comment
    # if comment_id:
    #     comment = []
    #     comment.append(Comment.objects.get(id = comment_id))
    #     ranked_comments = comment


    # Nested comments
    replies = list(get_reply_list(ranked_comments, rankby=rankby))
        
    return replies
