from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import StoryForm, ChapterForm
from .models import Story, Chapter, Hub
from profiles.models import User

def stories(request):
    story_list = Story.objects.all().order_by('-pub_date')

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

    # if not request.user.is_anonymous():
    #     subscribed_to = request.user.subscribed_to.all()
    # else:
    #     subscribed_to = []
    
    # Disable upvoted/downvoted
    # if request.user.is_authenticated():
    #     upvoted = request.user.upvoted.all()
    #     downvoted = request.user.downvoted.all()                
    # else:
    #     upvoted = []
    #     downvoted = []        
    
    return render(request, 'stories/stories.html',{
        'stories':stories,
        # 'upvoted': upvoted,
        # 'downvoted': downvoted,                
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
        'hubs':hubs
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
