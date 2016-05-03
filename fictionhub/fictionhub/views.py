
# to count words(refactor)
import re
from string import punctuation

from django.http import HttpResponseRedirect, HttpResponse

from django.shortcuts import render
from django.db.models import Count

from posts.models import Post
from posts.utils import rank_hot, rank_top, check_if_rational, check_if_daily
from hubs.models import Hub

def home(request):
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

    if check_if_daily(request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/write/')        
        return render(request, 'home-daily.html', {})
        
    if request.user.is_authenticated():
        return HttpResponseRedirect('/browse/')        
        
    # fictionhub includes rational        
    if rational:
        posts = Post.objects.filter(published=True, rational=rational, post_type="story")
    else:
        posts = Post.objects.filter(published=True, post_type="story")

    # Approved only
    posts = posts.filter(author__approved=True)
        
    # Count words
    r = re.compile(r'[{}]'.format(punctuation))
    for post in posts:
        wordcount = 0
        text = r.sub(' ',post.body)
        wordcount += len(text.split())
        if post.children:
            for child in post.children.all():
                text = r.sub(' ',child.body)
                wordcount += len(text.split())
        if wordcount > 1000:
            wordcount = str(int(wordcount/1000)) + "K"
        post.wordcount = wordcount

    # fictionhub doesn't include rational
    # posts = Post.objects.filter(published=True, rational=rational, post_type="story")    
    timespan="all-time"
    hot_posts = rank_hot(posts, top=32)[:10]
    top_posts = rank_top(posts, timespan = timespan)[:10]
    new_posts = posts.order_by('-pub_date')[:10]
    # hubs = Hub.objects.all().annotate(number_of_posts=Count('posts')).order_by('-number_of_posts')
    hubs = Hub.objects.all()



    # Add attribute:
    # for hub in hubs:
    #     stories = hub.posts.filter(published = True, rational = rational)
    #     hub.storycount = stories.count()
    # hubs_storycount = []
    # for hub in hubs:
    #     stories = hub.posts.filter(published = True, rational = rational)
    #     hub.storycount = stories.count()
    #     hubs_storycount.append(hub)

    # hubs = 
    # hubs = hubs_storycount.order_by('storycount')


    return render(request, 'home.html', {
        'hot_posts': top_posts, # hot_posts,
        'new_posts':new_posts,
        'hubs':hubs
    })

def test(request):
    test = request.META['HTTP_HOST']
    return render(request, 'test.html', {
        'test':test,
        'domain':request.META['HTTP_HOST']
})


def about(request):
    return render(request, 'about.html', {
})
