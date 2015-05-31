import datetime, re # praw
from django.utils.timezone import utc

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import StoryForm, ChapterForm
from .models import Story, Chapter, Hub
from profiles.models import User

def rank_hot(top=180, consider=1000, hub_slug=None):
    # top - number of stories to show,
    # consider - number of latest stories to rank
    
    def score(post, gravity=1.8, timebase=120):
        # number_of_comments = len(post.comments.all())
        rating = (post.score + 1)**0.8 # + number_of_comments
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        age = int((now - post.pub_date).total_seconds())/60
        return rating/(age+timebase)**1.8

    stories = Story.objects.all()

    # filter by hub
    # if hub_slug: 
    #     hub = Hub.objects.get(slug=hub_slug)
    #     stories_in_hub = []
    #     for post in stories:
    #         if hub in post.hubs.all():
    #             stories_in_hub.append(post)
    #     stories = stories_in_hub

    latest_stories = stories.order_by('-pub_date')#[:consider]
    #comprehension, stories with rating, sorted
    stories_with_rating = [(score(story), story) for story in latest_stories]
    ranked_stories = sorted(stories_with_rating, reverse = True)
    #strip away the rating and return only stories
    return [story for _, story in ranked_stories][:top]

def rank_top(timespan = None):
    stories = Story.objects.all()

    if timespan == "day":
        day = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('day')
        stories = stories.filter(pub_date__day = day)        
    elif timespan == "month":
        month = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('month')
        stories = stories.filter(pub_date__month = month)        
    elif timespan == "all-time":
        year = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('year')
        stories = stories.filter(pub_date__year = year)                
    
    top_stories = stories.order_by('-score')
    return top_stories


def stories(request, rankby="hot", timespan="all-time"):
    if rankby == "hot":
        story_list = rank_hot(top=32)
    elif rankby == "top":
        story_list = rank_top(timespan = timespan)
    elif rankby == "new":
        story_list = Story.objects.all().order_by('-pub_date')
    else:
        story_list = []

    # Pagination
    paginator = Paginator(story_list, 25)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stories = paginator.page(paginator.num_pages)    

    # Disable upvoted/downvoted
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        
    
    return render(request, 'stories/stories.html',{
        'stories':stories,
        'upvoted': upvoted,
        'downvoted': downvoted,
        'rankby': rankby,
        'timespan': timespan,                        
    })

def user_stories(request, username):
    userprofile = get_object_or_404(User, username=username)    
    story_list = Story.objects.filter(author=userprofile).order_by('-pub_date')

    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []

    # Pagination
    paginator = Paginator(story_list, 25)
    page = request.GET.get('page')
    try:
        stories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        stories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        stories = paginator.page(paginator.num_pages)    
    
    
    # Disable upvoted/downvoted
    # if request.user.is_authenticated():
    #     upvoted = request.user.upvoted.all()
    #     downvoted = request.user.downvoted.all()                
    # else:
    #     upvoted = []
    #     downvoted = []        
    
    return render(request, 'stories/user-stories.html',{
        'stories':stories,
        # 'upvoted': upvoted,
        # 'downvoted': downvoted,                
        'userprofile':userprofile,
        'subscribed_to': subscribed_to
    })


# Voting
def upvote(request):
    story = get_object_or_404(Story, id=request.POST.get('post-id'))
    story.score += 1
    story.save()
    story.author.karma += 1
    story.author.save()
    user = request.user
    user.upvoted.add(story)
    user.save()
    return HttpResponse()

def downvote(request):
    story = get_object_or_404(Story, id=request.POST.get('post-id'))
    if story.score > 0:
        story.score -= 1
        story.author.karma -= 1        
    story.save()
    story.author.save()
    user = request.user
    user.downvoted.add(story)
    user.save()
    return HttpResponse()


def story(request, story):
    story = Story.objects.get(slug=story)
    # comments = Comment.objects.filter(post = post)                

    try:
        first_chapter = Chapter.objects.get(story=story, number=1)
    except:
        first_chapter = []
    
    hubs = story.hubs.all()
    
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False) # return story but don't save it to db just yet
    #         comment.author = request.user
    #         comment.parent = None
    #         comment.post = post
    #         comment.save()
    #         return HttpResponseRedirect('/post/'+slug+'#comments')
    # else:
    #     form = CommentForm()

    # if request.user.is_authenticated():
    #     upvoted = request.user.upvoted.all()
    #     downvoted = request.user.downvoted.all()                
    # else:
    #     upvoted = []
    #     downvoted = []  

    return render(request, 'stories/story.html',{
        'story': story,
        # 'upvoted': upvoted,
        # 'downvoted': downvoted,
        'first_chapter':first_chapter,
        # 'comments': comments,        
        # 'form': form,
        'hubs':hubs
    })


def chapter(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter)    
    # comments = Comment.objects.filter(post = post)                

    try:
        prev_chapter = Chapter.objects.get(story=story, number=chapter.number-1)
    except:
        prev_chapter = []

    try:
        next_chapter = Chapter.objects.get(story=story, number=chapter.number+1)
    except:
        next_chapter = []

    hubs = story.hubs.all()
    
    # if request.method == 'POST':
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False) # return story but don't save it to db just yet
    #         comment.author = request.user
    #         comment.parent = None
    #         comment.post = post
    #         comment.save()
    #         return HttpResponseRedirect('/post/'+slug+'#comments')
    # else:
    #     form = CommentForm()

    
    # if request.user.is_authenticated():
    #     upvoted = request.user.upvoted.all()
    #     downvoted = request.user.downvoted.all()                
    # else:
    #     upvoted = []
    #     downvoted = []        
        
    
    return render(request, 'stories/chapter.html',{
        'story': story,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,       
        # 'upvoted': upvoted,
        # 'downvoted': downvoted,        
        # 'comments': comments,        
        # 'form': form,
        'hubs':hubs,
    })


def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False) # return story but don't save it to db just yet
            story.author = request.user
            story.save()
            story.hubs.add(*form.cleaned_data['hubs'])
            return HttpResponseRedirect('/story/'+story.slug+'/edit')
    else:
        form = StoryForm()
    return render(request, 'stories/story-create.html', {'form':form})


def chapter_create(request, story):
    story = Story.objects.get(slug=story)    
    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            # return HttpResponseRedirect('/asdf')                
            chapter = form.save(commit=False) # return story but don't save it to db just yet
            chapter.story = story
            chapter.number = story.chapters.count()+1
            chapter.save()
            return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'/edit')
    else:
        form = ChapterForm()
        
    return render(request, 'stories/edit.html', {
        'story':story,        
        'form':form,
        'action':'chapter_create'        
    })


def story_edit(request, story):
    story = Story.objects.get(slug=story)

    if request.method == 'POST':
        form = StoryForm(request.POST,instance=story)
        if form.is_valid():
            story = form.save(commit=False) # return story but don't save it to db just yet
            story.save()
            return HttpResponseRedirect('/story/'+story.slug+'/edit')
    else:
        form = StoryForm(instance=story)
    
    return render(request, 'stories/edit.html', {
        'story':story,
        'form':form,
        'action':'story_edit'
    })

def chapter_edit(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter)

    if request.method == 'POST':
        form = ChapterForm(request.POST,instance=chapter)
        if form.is_valid():
            chapter = form.save(commit=False) # return story but don't save it to db just yet
            chapter.save()
            return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'/edit')
    else:
        form = ChapterForm(instance=chapter)
    
    return render(request, 'stories/edit.html', {
        'story':story,
        'chapter':chapter,
        'form':form,
        'action':'chapter_edit'                
    })

def chapter_up(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter) # add story=story, to not confuse with others!
    try:
        following_chapter = story.chapters.get(number=chapter.number+1)
        following_chapter.number -= 1
        following_chapter.save()
    except:
        pass

    chapter.number += 1
    chapter.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))            

def chapter_down(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter) # add story=story, to not confuse with others!

    if chapter.number > 0:    
        try:
            following_chapter = story.chapters.get(number=chapter.number-1)
            following_chapter.number += 1
            following_chapter.save()
        except:
            pass

        chapter.number -= 1
        chapter.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def chapter_delete(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter) # add story=story, to not confuse with others!
    chapter.delete()
    return HttpResponseRedirect('/story/'+story.slug+'/edit')    

def story_delete(request, story):
    story = Story.objects.get(slug=story)
    story.delete()
    return HttpResponseRedirect('/') # to story list
