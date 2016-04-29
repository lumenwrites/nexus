import datetime
import time
import praw    
import re, random
from django.utils.timezone import utc

from django.utils.timezone import utc
from django.shortcuts import get_object_or_404

from posts.models import Post
from hubs.models import Hub
from profiles.models import User

def rank_hot(stories, top=180, consider=1000):
    # top - number of stories to show,
    # consider - number of latest stories to rank
    
    def score(post, gravity=1.8, timebase=120):
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


def check_if_daily(request):
    daily = False
    if request.META['HTTP_HOST'] == "daily.fictionhub.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        daily = True
    return daily






def age(timestamp):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    # usage: age(prompt.created_utc)
    return age_in_minutes

def get_prompts():
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=128)
    new_prompts = list(prompts)
    prompts = []


    hot_prompts = list(subreddit.get_hot(limit=50))
    
    max_age = 5*60
    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        # 1 4 5*60
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 3) \
        and (age(prompt.created_utc) < max_age):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompt.age = round(age(prompt.created_utc)/60,1)
            # prompt.permalink = prompt.permalink.replace("www", "zn")
            prompt.sort = prompt.score * (1-(prompt.age/5))

            # prompt position
            for index, p in enumerate(hot_prompts):
                if prompt.title == p.title:
                    setattr(prompt, "position", index)
                    # prompt.position == index

            prompt.title = prompt.title.replace("[WP]", "", 1).strip()   
            prompts.append(prompt)
                


    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)

    return prompts[:16]




# def filter_posts(request, filterby,rational,hubslug):
#     hub = []
#     if filterby == "subscriptions":
#         subscribed_to = request.user.subscribed_to.all()
#         posts = Post.objects.filter(author=subscribed_to, published=True, rational = rational)
#         filterurl="/subscriptions" # to add to href  in subnav
#     elif filterby == "hub":
#         hub = Hub.objects.get(slug=hubslug)
#         # Show posts from all the children hubs? Don't know how to sort.
#         # children = Hub.objects.filter(parent=hub)
#         # hubs = []
#         if hubslug == "wiki":
#             posts = Post.objects.filter(hubs=hub, published=True,
#                                         post_type = "wiki")
#             post_type = "wiki"
#         else:
#             posts = Post.objects.filter(hubs=hub, published=True, post_type = "story") #  rational = rational, 
#         filterurl="/hub/"+hubslug # to add to href  in subnav
#     elif filterby == "user":
#         userprofile = get_object_or_404(User, username=username)
#         if request.user == userprofile:
#             # If it's my profile - display all the posts, even unpublished.
#             # fictionhub includes rational        
#             if rational:
#                 posts = Post.objects.filter(author=userprofile,
#                                             rational=rational).exclude(post_type="chapter")
#             else:
#                 posts = Post.objects.filter(author=userprofile).exclude(post_type="chapter")
#             # , post_type="story")
#         else:
#             # fictionhub includes rational        
#             if rational:
#                 posts = Post.objects.filter(author=userprofile,
#                                             rational=rational,
#                                             published=True).exclude(post_type="chapter")
#             else:
#                 posts = Post.objects.filter(author=userprofile,
#                                             published=True)
#         filterurl="/user/"+userprofile.username # to add to href  in subnav
#     elif filterby == "challenges":
#         posts = Post.objects.filter(post_type = "challenge", published=True, rational = rational)
#         rankby = "new"
#     elif filterby == "challenge":
#         challenge = Post.objects.get(slug=challenge)
#         if challenge.state == "voting":
#             rankby = "new" # later do random
#         elif challenge.state == "completed":            
#             rankby = "top"
#         posts = Post.objects.filter(parent=challenge, published=True, rational = rational)
#     elif filterby == "prompt":
#         prompt = Post.objects.get(slug=prompt)
#         posts = Post.objects.filter(parent=prompt)#, published=True, rational = rational)
#         rankby = "hot"
#     else:
#         # fictionhub includes rational        
#         if rational:
#             posts = Post.objects.filter(published=True, rational = rational, post_type="story")
#         else:
#             posts = Post.objects.filter(published=True, post_type="story")
#         # fictionhub doesn't include rational
#         # posts = Post.objects.filter(published=True, rational = rational, post_type="story")
#         filterurl="/stories"
    
#     return posts, filterurl, hub
