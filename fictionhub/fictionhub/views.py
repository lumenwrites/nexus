from django.shortcuts import render
from django.db.models import Count

from posts.models import Post
from posts.utils import rank_hot, rank_top
from hubs.models import Hub

def home(request):
    posts = Post.objects.filter(published=True)    
    hot_posts = rank_hot(posts, top=32)[:10]
    new_posts = posts.order_by('-pub_date')[:10]
    hubs = Hub.objects.all().annotate(number_of_posts=Count('posts')).order_by('-number_of_posts')
    return render(request, 'home.html', {
        'hot_posts':hot_posts,
        'new_posts':new_posts,
        'hubs':hubs
    })

def test(request):
    return render(request, 'test.html')
