import re # praw

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext

# Forms
from .forms import StoryForm, ChapterForm
from comments.forms import CommentForm
from hubs.forms import HubForm

# Models
from .models import Story, Chapter
from profiles.models import User
from hubs.models import Hub
from comments.models import Comment

# rss
from xml.etree.ElementTree import Element, SubElement, tostring
from django.core.urlresolvers import *

# json
import json

# utility functions
from comments.utils import get_comment_list
from .utils import rank_hot, rank_top

def stories(request, rankby="hot", timespan="all-time",
            filterby="", hubslug="", username=""):
    # for user profile navbar
    userprofile = []
    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []
    
    if filterby == "subscriptions":
        subscribed_to = request.user.subscribed_to.all()
        stories = Story.objects.filter(author=subscribed_to, published=True)
        filterurl="/subscriptions" # to add to href  in subnav
    elif filterby == "hub":
        hub = Hub.objects.get(slug=hubslug)
        # Show stories from all the children hubs? Don't know how to sort.
        # children = Hub.objects.filter(parent=hub)
        # hubs = []
        stories = Story.objects.filter(hubs=hub, published=True)
        filterurl="/hub/"+hubslug # to add to href  in subnav
    elif filterby == "user":
        userprofile = get_object_or_404(User, username=username)
        if request.user == userprofile:
            # If it's my profile - display all the stories, even unpublished.
            stories = Story.objects.filter(author=userprofile)
        else:
            stories = Story.objects.filter(author=userprofile, published=True)
        filterurl="/user/"+username # to add to href  in subnav
    else:
        stories = Story.objects.filter(published=True)
        filterurl="" # to add to href  in subnav                

    if rankby == "hot":
        story_list = rank_hot(stories, top=32)
    elif rankby == "top":
        story_list = rank_top(stories, timespan = timespan)
    elif rankby == "new":
        story_list = stories.order_by('-pub_date')
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

    
    # if not stories:
    #     return HttpResponseRedirect('/404')

    hubs = Hub.objects.all().order_by('id')

    return render(request, 'stories/stories.html',{
        'stories':stories,
        'upvoted': upvoted,
        'downvoted': downvoted,
        'filterby':filterby,
        'filterurl': filterurl,                
        'rankby': rankby,
        'timespan': timespan,
        'userprofile':userprofile,
        'subscribed_to': subscribed_to,
        'hubs': hubs
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

def unupvote(request):
    story = get_object_or_404(Story, id=request.POST.get('post-id'))
    story.score -= 1
    story.save()
    story.author.karma = 1
    story.author.save()
    user = request.user
    user.upvoted.remove(story)
    user.save()
    return HttpResponse()

def undownvote(request):
    story = get_object_or_404(Story, id=request.POST.get('post-id'))
    story.score += 1
    story.author.karma += 1        
    story.save()
    story.author.save()
    user = request.user
    user.downvoted.remove(story)
    user.save()
    return HttpResponse()
            
def story(request, story, comment_id="", chapter="", rankby="new"):
    try:
        story = Story.objects.get(slug=story)
    except:
        return HttpResponseRedirect('/404')
        

    try:
        first_chapter = Chapter.objects.get(story=story, number=1)
    except:
        first_chapter = []
    

    # If chapter
    if chapter:
        chapter = Chapter.objects.get(slug=chapter)
        first_chapter = []  # empty first chapter to show the right button in story template
        try:
            prev_chapter = Chapter.objects.get(story=story, number=chapter.number-1)
        except:
            prev_chapter = []

        try:
            next_chapter = Chapter.objects.get(story=story, number=chapter.number+1)
        except:
            next_chapter = []
    else:
        chapter = []
        prev_chapter = []
        next_chapter = []
        
    
    hubs = story.hubs.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # return story but don't save it to db just yet
            comment.author = request.user
            comment.parent = None
            if chapter:
                comment.chapter = chapter                
            else:
                comment.story = story
            comment.save()
            if chapter:
                return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'#comments')
            else:
                return HttpResponseRedirect('/story/'+story.slug+'#comments')
    else:
        form = CommentForm()

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []  

    # For subscribe button
    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []

        
    # Get top lvl comments
    if chapter:
        top_lvl_comments = Comment.objects.filter(chapter = chapter, parent = None)
    else:
        top_lvl_comments = Comment.objects.filter(story = story, parent = None)

    # Rank comments
    if rankby == "hot":
        ranked_comments = rank_hot(top_lvl_comments, top=32)
    elif rankby == "top":
        ranked_comments = rank_top(top_lvl_comments, timespan = "all-time")
    elif rankby == "new":
        ranked_comments = top_lvl_comments.order_by('-pub_date')
    else:
        ranked_comments = []

    # Permalink to one comment
    if comment_id:
        comment = []
        comment.append(Comment.objects.get(id = comment_id))
        ranked_comments = comment


    # Nested comments
    comments = list(get_comment_list(ranked_comments, rankby=rankby))

    if request.user.is_authenticated():
        comments_upvoted = request.user.comments_upvoted.all()
        comments_downvoted = request.user.comments_downvoted.all()                
    else:
        comments_upvoted = []
        comments_downvoted = []  

    return render(request, 'stories/story.html',{
        'story': story,
        'first_chapter':first_chapter,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,       
        'upvoted': upvoted,
        'downvoted': downvoted,
        'comments_upvoted': comments_upvoted,
        'comments_downvoted': comments_downvoted,
        'comments': comments,
        'rankby': rankby,        
        'form': form,
        'hubs':hubs,
        'subscribed_to':subscribed_to        
    })

def chapter_back(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter)    
    comments = Comment.objects.filter(chapter = chapter)                

    try:
        prev_chapter = Chapter.objects.get(story=story, number=chapter.number-1)
    except:
        prev_chapter = []

    try:
        next_chapter = Chapter.objects.get(story=story, number=chapter.number+1)
    except:
        next_chapter = []

    hubs = story.hubs.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # return story but don't save it to db just yet
            comment.author = request.user
            comment.parent = None
            # comment.story = story
            comment.chapter = chapter            
            comment.save()
            return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'#comments')
    else:
        form = CommentForm()

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        
    
    return render(request, 'stories/chapter.html',{
        'story': story,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,       
        'upvoted': upvoted,
        'downvoted': downvoted,        
        'comments': comments,        
        'form': form,
        'hubs':hubs,
    })


def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False) # return story but don't save it to db just yet
            story.author = request.user
            # self upvote
            story.score += 1
            story.save()
            request.user.upvoted.add(story)            
            story.hubs.add(*form.cleaned_data['hubs'])
            hubs = story.hubs.all()
            for hub in hubs:
                if hub.parent:
                    story.hubs.add(hub.parent)
            # Hacky way to 
            # for hub in form.cleaned_data['hubs']:
            #     if hub.parent:
            #         story.hubs.add(hub.parent)
            #         if hub.parent.parent:
            #             story.hubs.add(hub.parent.parent)
            return HttpResponseRedirect('/story/'+story.slug+'/edit')
    else:
        form = StoryForm()
        form.fields["hubs"].queryset = Hub.objects.filter(children=None).order_by('id')

    return render(request, 'stories/story-create.html', {
        'form':form,
        'hubs':Hub.objects.all()
    })


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

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        form = StoryForm(request.POST,instance=story)
        if form.is_valid():
            story = form.save(commit=False) # return story but don't save it to db just yet
            story.save()
            story.hubs = []
            story.hubs.add(*form.cleaned_data['hubs'])
            hubs = story.hubs.all()
            for hub in hubs:
                if hub.parent:
                    story.hubs.add(hub.parent)
            return HttpResponseRedirect('/story/'+story.slug+'/edit')
    else:
        form = StoryForm(instance=story)
        form.fields["hubs"].queryset = Hub.objects.filter(children=None).order_by('id')        
    
    return render(request, 'stories/edit.html', {
        'story':story,
        'form':form,
        'action':'story_edit'
    })

def chapter_edit(request, story, chapter):
    story = Story.objects.get(slug=story)
    chapter = Chapter.objects.get(slug=chapter)

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        
    
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

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

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

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

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

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    chapter.delete()
    return HttpResponseRedirect('/story/'+story.slug+'/edit')    

def story_delete(request, story):
    story = Story.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    story.delete()
    return HttpResponseRedirect('/') # to story list

def story_publish(request, story):
    story = Story.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    story.published = True
    story.save()
    return HttpResponseRedirect('/story/'+story.slug+'/edit')

def story_unpublish(request, story):
    story = Story.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != story.author:
        return HttpResponseRedirect('/')        

    story.published = False
    story.save()
    return HttpResponseRedirect('/story/'+story.slug+'/edit')




def page_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def story_feed(request, story):
    story = Story.objects.get(slug=story)
    rss = Element('rss')
    rss.set("version","2.0")

    channel = SubElement(rss,'channel')

    title = SubElement(channel,'title')
    title.text = story.title

    link = SubElement(channel,'link')
    link.text = "http://fictionhub.io/story/"+story.slug # request.build_absolute_uri(reverse("story"))

    desc = SubElement(channel,'description')
    desc.text = story.description

    chapters = story.chapters.all()

    for index in chapters:
        item = SubElement(channel,'item')

        title_c = SubElement(item,'title')
        title_c.text = index.title
        
        link = SubElement(item,'link')
        #link.text = request.build_absolute_uri(index.get_absolute_url())
        link.text = "http://fictionhub.io/story/"+story.slug
    return HttpResponse(tostring(rss, encoding='UTF-8'), content_type='application/xml')


def story_json(request, slug):
    try:
        story = Story.objects.get(slug=slug)
    except:
        return HttpResponseRedirect('/404')

    res = {}
    res['title'] = story.title
    res['author'] = story.author.username
    res['chapters'] = []
    chapters = story.chapters.all()

    for index in chapters:
        res['chapters'].append({"title": index.title, "number": index.number, "text": index.body})

    return HttpResponse(json.dumps(res), content_type='application/json')