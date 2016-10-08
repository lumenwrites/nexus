# standard library imports
import re, random
from string import punctuation
from math import floor # to round views
from html2text import html2text
# date
from datetime import datetime
from time import mktime
#dropbox
import os
from markdown import Markdown
import time


# core django components
# CBVs
from django.views.generic import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import * # for rss
from django.core.mail import send_mail # for email
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.timezone import utc

from django.conf import settings


# My own stuff
# utility functions
from comments.utils import get_comment_list, get_comments, submit_comment
from .utils import rank_hot, rank_top, check_if_rational, check_if_daily, check_if_fictionhub
from .utils import get_prompts, age, stats
from .utils import count_words
from .shortcuts import get_or_none
# Forms
from .forms import PostForm, PromptForm
from comments.forms import CommentForm
from hubs.forms import HubForm
# Models
from .models import Post
from core.models import Util
from profiles.models import User
from hubs.models import Hub
from comments.models import Comment
from notifications.models import Message
from challenges.models import Prompt




class FilterMixin(object):
    paginate_by = 15
    def get_queryset(self):
        qs = super(FilterMixin, self).get_queryset()


        # Filter by hubs
        try:
            selectedhubs = self.request.GET['hubs'].split(",")
        except:
            selectedhubs = []
        filterhubs = []
        if selectedhubs:
            for hubslug in selectedhubs:
                filterhubs.append(Hub.objects.get(slug=hubslug))
        for hub in filterhubs:
            qs = qs.filter(hubs=hub)            


        # Filter by query
        query = self.request.GET.get('query')
        if query:
            qs = qs.filter(Q(title__icontains=query) |
                           Q(body__icontains=query) |
                           Q(author__username__icontains=query))                    

        # Sort
        # (Turns queryset into the list, can't just .filter() later
        sorting = self.request.GET.get('sorting')
        if sorting == 'top':
            qs = qs.order_by('-score')
        elif sorting == 'new':
            qs = qs.order_by('-pub_date')
        else:
            qs = rank_hot(qs)

        return qs

    def get_context_data(self, **kwargs):
        context = super(FilterMixin, self).get_context_data(**kwargs)
        urlstring = ""
        # Sorting
        if self.request.GET.get('sorting'):
            sorting = self.request.GET.get('sorting')
        else:
            sorting = "hot"
        context['sorting'] = sorting

        # urlstring = self.request.path + "?sorting=" + sorting
            

        # Filtered Hubs
        try:
            selectedhubs = self.request.GET['hubs'].split(",")
        except:
            selectedhubs = []
        filterhubs = []
        if selectedhubs:
            for hubslug in selectedhubs:
                filterhubs.append(Hub.objects.get(slug=hubslug))
        context['filterhubs'] = filterhubs
        # All Hubs
        context['hubs'] = Hub.objects.all()
        # Solo Hub
        context['hub'] = self.request.GET.get('hub')


        if filterhubs:
            hublist = ",".join([hub.slug for hub in filterhubs])
            urlstring += "&hubs=" + hublist

        # Query
        query = self.request.GET.get('query')
        if query:
            context['query'] = query
            urlstring += "&query=" + query            

        context['urlstring'] = urlstring

        return context
    



class BrowseView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def dispatch(self, request, *args, **kwargs):
        # Redirect to wst homepage
        if not request.user.is_authenticated() and request.path == "/":
            return render(request, 'home.html', {})
        else:
            return super(BrowseView, self).dispatch(request, *args, **kwargs)
       
        
    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()        
        # qs = [p for p in qs if (p.published == True and
        #                         p.author.approved ==True)]

        return qs

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['form'] = PostForm()
        if self.request.user.is_authenticated():
            context['userprofile'] = self.request.user
        return context    
    

class UserprofileView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(UserprofileView, self).get_queryset()

        # Filter by user
        userprofile = User.objects.get(username=self.kwargs['username'])        
        qs = [p for p in qs if (p.author==userprofile)]

        # Show only published to everyone else
        # if self.request.user != userprofile:
        #     qs = [p for p in qs if (p.published==True)]            
        
        return qs

    def get_context_data(self, **kwargs):
        context = super(UserprofileView, self).get_context_data(**kwargs)
        userprofile = User.objects.get(username=self.kwargs['username'])        
        context['userprofile'] = userprofile

        # Sorting
        if self.request.GET.get('sorting'):
            sorting = self.request.GET.get('sorting')
        else:
            sorting = "new"
        context['sorting'] = sorting
        

        view_count = 0
        for post in userprofile.posts.all():
            view_count += post.views
        if view_count > 1000:
            view_count = str(floor(view_count/1000)) + "K"
        context['view_count'] = view_count
                
        score = 0        
        for post in userprofile.posts.all():
            score += post.score
        if score > 1000:
            score = str(int(score/1000)) + "K"
        context['score'] = score


        
        return context    
    

class SubscriptionsView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(SubscriptionsView, self).get_queryset()
        
        # Filter by subscriptions
        user = self.request.user
        subscribed_to = []
        if user.is_authenticated():
            subscribed_to = self.request.user.subscribed_to.all()
        
        qs = [p for p in qs if (p.author in subscribed_to)]
        
        return qs
        


class HubView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def get_queryset(self):
        qs = super(HubView, self).get_queryset()

        # Filter by hub
        hub = Hub.objects.get(slug=self.kwargs['hubslug'])

        # qs = [p for p in qs if (hub in p.hubs.all())]

        posts = []
        for post in qs:
            for h in post.hubs.all():
                if h.slug==hub.slug:
                    posts.append(post)
        qs = posts

        return qs
        
    def get_context_data(self, **kwargs):
        context = super(HubView, self).get_context_data(**kwargs)
        hub = Hub.objects.get(slug=self.kwargs['hubslug'])
        context['hubtitle'] = hub.title
        return context    
    


class HubList(ListView):
    model = Hub
    template_name = "hubs/hubs.html"


class SeriesList(ListView):
    model = Post
    template_name = "series/series.html"
    paginate_by=15
    



    


# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    post.author.karma += 1
    post.author.save()
    user = request.user
    user.upvoted.add(post)
    user.save()

    # Notification
    message = Message(from_user=request.user,
                      to_user=post.author,
                      story=post,
                      message_type="upvote")
    message.save()
    post.author.new_notifications = True
    post.author.save()
    return HttpResponse()

def unupvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score -= 1
    post.save()
    post.author.karma -= 1
    post.author.save()
    user = request.user
    user.upvoted.remove(post)
    user.save()
    return HttpResponse()



def post(request, slug, comment_id="", rankby="new", filterby=""):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])

    post = get_object_or_404(Post, slug=slug)
        
    # comments = get_comments(post=post)

    # # Permalink to one comment
    # if comment_id:
    #     comments = get_comments(post=post, comment_id=comment_id)

    # # Submit comments
    # if request.method == 'POST':
    #         submit_comment(request, post)            
    # form = CommentForm()

    # Footer info
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        subscribed_to = request.user.subscribed_to.all()
    else:
        upvoted = []
        subscribed_to = []

    hubs = post.hubs.all()        

    # Increment views counter. Do clever memcache laters.
    if not request.user.is_staff and request.user != post.author:
        post.views +=1
        post.save()

    # Just for private website subheader
    userprofile = post.author

    return render(request, 'posts/post.html',{
        'post': post,
        'upvoted': upvoted,
        'rankby': rankby,        
        'hubs':hubs,
        'subscribed_to':subscribed_to,
        'userprofile':userprofile,        
    })

def post_create(request, story="", challenge="", prompt="", posttype="", hubslug=""):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            # Create new story
            post = form.save(commit=False)
            post.author = request.user
            post.score += 1 # self upvote

            post.save()
            request.user.upvoted.add(post)

            hubs_string = request.POST.get('hubs')
            hubs_list = hubs_string.split("#")
            for hubslug in hubs_list:
                if hubslug:
                    hubslug = hubslug.strip()
                    hub, created = Hub.objects.get_or_create(title=hubslug,slug=hubslug)
                    post.hubs.add(hub)

            # Add hubs
            post.hubs.add()
            hubs = post.hubs.all()

            return HttpResponseRedirect('/') # story/'+post.slug+'/edit'
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {
            'form':form,
            'hubs':Hub.objects.all(),
            'hubslug':hubslug,                                    
            'test': ""
        })


def post_edit(request, story, chapter=""):
    story = Post.objects.get(slug=story)
    action = "story_edit"
    if chapter:
        chapter = Post.objects.get(parent=story,slug=chapter)
        action="chapter_edit"

    rational = check_if_rational(request)
    daily = check_if_daily(request)    

    # throw him out if he's not an author
    if request.user != story.author and not request.user.is_staff and story.post_type != "wiki":
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        if chapter:
            form = PostForm(request.POST,instance=chapter, storyslug=story.slug)            
        else:
            form = PostForm(request.POST,instance=story, storyslug=story.slug)
        if form.is_valid():
            post = form.save(commit=False) # return post but don't save it to db just yet
            # post.post_type = "story"
            post.rational = rational
            post.daily = daily            

            if chapter:
                post.post_type = "chapter"
                post.parent = story

            if chapter:
                post.save(slug=chapter.slug)
            else:
                post.save(slug=story.slug)                

            post.hubs = []
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            for hub in hubs:
                if hub.parent and hub.parent.hub_type != "folder":
                    post.hubs.add(hub.parent)
                    if hub.parent.parent and hub.parent.parent.hub_type != "folder":
                        post.hubs.add(hub.parent.parent)
            if chapter:
                return HttpResponseRedirect('/story/'+story.slug+'/'+post.slug+'/edit')
            else:
                return HttpResponseRedirect('/story/'+post.slug+'/edit')
    else:
        if chapter:
            form = PostForm(instance=chapter, storyslug=story.slug)    
        else:
            form = PostForm(instance=story, storyslug=story.slug)
        form.fields["hubs"].queryset = Hub.objects.filter(hub_type="hub")
        # filter(children=None).order_by('id')

    return render(request, 'posts/edit.html', {
        'story':story,
        'chapter':chapter,            
        'form':form,
        'action':action
    })


def post_delete(request, story, chapter=""):
    story = Post.objects.get(slug=story)
    if chapter:
        post = Post.objects.get(parent=story,slug=chapter)
    else:
        post = story

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.delete()
    if chapter:
        return HttpResponseRedirect('/story/'+story.slug + '/edit') # to post list
    else:
        return HttpResponseRedirect('/') # to post list


def post_publish(request, story):
    post = Post.objects.get(slug=story)

    # throw him out if he's not an author

    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = True
    post.save()

    # if request.user.username == "rayalez":
    #     return HttpResponseRedirect(post.get_absolute_url()+"/wprepost")                

    # Send Email
    # author = post.author
    # subscribers = author.subscribers.all()
    # emails = []
    # for subscriber in subscribers:
    #     if subscribers.email_subscriptions:
    #         try:
    #             email = subscriber.email
    #             emails.append(email)
    #         except:
    #             pass
    # topic = author.username + " has published a new story to fictionhub"
    # body = "Hi! You are receiving this email because you have subscribed to updates about new stories written by " + author.username + " at fictionhub.io \n\n"
    # body += author.username + " has published a new story:\n'" + post.title + \
    #         "'\nYou can read it here:\n" + "http://fictionhub.io" + post.get_absolute_url()
    # body += "\n\nYou can manage your email notifications in preferences:\n" +\
    #         "http://fictionhub.io/preferences/"
    # body += "\n\n P.S. \n fictionhub, including email notifications, is still in beta. If you have any questions or suggestions - feel free to reply to this message, I welcome any feedback."
    # send_mail(topic, body, 'raymestalez@gmail.com', emails, fail_silently=False)

    # Notification
    if not check_if_daily(request):
        subscribers = post.author.subscribers.all()
        for subscriber in subscribers:
            message = Message(from_user=post.author,
                              to_user=subscriber,
                              story=post,
                              message_type="newstory")
            message.save()
            subscriber.new_notifications = True
            subscriber.save()

    return HttpResponseRedirect('/story/'+post.slug+'/edit')


def post_unpublish(request, story):
    post = Post.objects.get(slug=story)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.published = False
    post.save()
    return HttpResponseRedirect('/story/'+post.slug+'/edit')

    
    
def email(request):
    send_mail('My awesome email', 'Oh hell yeah..', 'raymestalez@gmail.com', ['raymestalez@gmail.com'], fail_silently=False)
    return HttpResponse("Yes!")


def item(request):
    test=""
    return render(request, 'store/single-item.html', {
        'test':test,
        'userprofile': User.objects.get(username="rayalez"),
})

def book(request):
    return render(request, 'store/cover.html', {
        'orangemind': True,
    })

def sandbox(request):
    posts = Post.objects.filter(published=True,author__approved=False).order_by('-pub_date')
    return render(request, 'posts/posts.html',{
        'posts':posts,
        'hubs': [],        
    })



    


# TODO: dry it in one function
# def vote(request):
#     post = Post.objects.get(id=request.POST.get('post-id'))
#     vote =  request.POST.get('vote')
#     user = request.user

#     if post in user.upvoted:    # unupvote
#         post.score -= 1
#         post.author.karma -= 1
#         user.upvoted.remove(post)
#     elif vote == "up":          # upvote
#         post.score += 1
#         post.author.karma += 1
#         user.upvoted.add(post)

#     post.save()
#     post.author.save()
#     user.save()

#     return HttpResponse()



    # Daily
def post_create_daily(request):
    rational = False
    test = ""
    prompt =""
    prompts = ""
    days = []
    longeststreak = 0
    currentstreak = 0
    wordcount = 0


    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    concepts = list(Prompt.objects.filter(Q(prompt_type="concept") | Q(prompt_type="prompt")  | Q(prompt_type="wpsub")))
    concepts= [p.prompt for p in concepts]
    random.shuffle(concepts)
    concepts = concepts[:16]
            
    settings = list(Prompt.objects.filter(prompt_type="setting"))
    settings= [p.prompt for p in settings]
    random.shuffle(settings)
    settings = settings[:16]

    characters = list(Prompt.objects.filter(prompt_type="character"))
    characters= [p.prompt for p in characters]
    random.shuffle(characters)
    characters = characters[:16]

    problems = list(Prompt.objects.filter(prompt_type="problem"))
    problems= [p.prompt for p in problems]
    random.shuffle(problems)
    problems = problems[:16]
        
    element = ["Opinion/Setup", "Phys", "Adj","Will","Because","Process",]
    element =  random.choice(element)    

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # self upvote
            post.score += 1
            post.post_type = "story"
            post.rational = False
            post.daily = True

            if request.user.username == "lumenwrites":
                post.published = True
                post.daily = False                            
            
            post.reddit_url = request.POST.get("reddit_url", "")
            post.save()
            request.user.upvoted.add(post)            
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            for hub in hubs:
                if hub.parent and hub.parent.hub_type != "folder":
                    post.hubs.add(hub.parent)
                    if hub.parent.parent and hub.parent.parent.hub_type != "folder":
                        post.hubs.add(hub.parent.parent)

            return HttpResponseRedirect('/story/'+post.slug+'/edit')
    else:
        form = PostForm()
        form.fields["hubs"].queryset = Hub.objects.filter(hub_type="hub")
        

        # Stats
        statsposts = Post.objects.filter(author=request.user, daily=check_if_daily(request))
        statsposts = statsposts.order_by('pub_date')
        days, longeststreak, currentstreak, wordcount = stats(statsposts)

        # Prompts
        prompts = list(Prompt.objects.all())
        random.shuffle(prompts)
        prompts = prompts[:16]
        prompt = prompts[0].prompt

        # Fetch writingprompts for me
        if request.user.username == "rayalez" or request.user.username == "lumenwrites":
            prompts = get_prompts()        


        if wordcount > 1000:
            wordcount = str(int(wordcount/1000)) + "K"
        
    return render(request, 'posts/create-daily.html', {
        'form':form,
        'hubs':Hub.objects.all(),
        'prompt':prompt,
        'prompts':prompts,
        'days':days,
        'wordcount':wordcount,        
        'longeststreak':longeststreak,
        'currentstreak':currentstreak,
        'concepts':concepts,        
        'settings':settings,
        'characters':characters,
        'problems':problems,
        'element':element,        
        'test': ""
    })    




    # prompts
def writing_prompts(request):
    prompts = get_prompts()
    prompts = prompts[:16]

    # random.shuffle(prompts)
    # prompts = prompts[:1]
    
    return render(request, 'posts/writing-prompts.html', {
        'prompts': prompts,
        'max_age': max_age,        
    })



