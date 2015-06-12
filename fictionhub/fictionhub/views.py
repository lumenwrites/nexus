from django.shortcuts import render
from django.db.models import Count

from stories.models import Story
from stories.utils import rank_hot, rank_top
from hubs.models import Hub

def home(request):
    stories = Story.objects.filter(published=True)    
    hot_stories = rank_hot(stories, top=32)[:10]
    new_stories = stories.order_by('-pub_date')[:10]
    hubs = Hub.objects.all().annotate(number_of_stories=Count('stories')).order_by('-number_of_stories')
    return render(request, 'home.html', {
        'hot_stories':hot_stories,
        'new_stories':new_stories,
        'hubs':hubs
    })

def test(request):
    return render(request, 'test.html')
