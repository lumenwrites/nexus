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

from django.db.models import Q, Count
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
from .utils import rank_hot, rank_top, check_if_rational, check_if_daily, check_if_fictionhub
from .utils import age, count_words
from .utils import get_replies, get_reply_list
from .shortcuts import get_or_none
# Forms
from .forms import PostForm, PromptForm
from hubs.forms import HubForm
# Models
from .models import Post
from profiles.models import User
from hubs.models import Hub
from notifications.models import Notification





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

        # Filter by hubs I'm subscribed to
        
        if self.request.GET.get('hubfilter') == "following":
            subscribed_to_hubs = self.request.user.subscribed_to_hubs
            qs = qs.filter(hubs__in=subscribed_to_hubs.all())   

        # Filter by posttype
        posttype = self.request.GET.get('posttype')
        if posttype == "post":
            qs = qs.filter(parent=None)   
        if posttype == "reply":
            qs = qs.filter(parent__isnull=False)   

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
        hubs = Hub.objects.all()
        hubs = Hub.objects.annotate(num_posts=Count('posts')).order_by('-num_posts')   
        context['hubs'] = hubs

        if self.request.GET.get('hubfilter') == "following":
            context['hubfilter'] = "following"

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

    def get_queryset(self):
        qs = super(BrowseView, self).get_queryset()        
        # qs = [p for p in qs if (p.published == True and
        #                         p.author.approved ==True)]

        return qs

    def get_context_data(self, **kwargs):
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['form'] = PostForm()
        return context    


class HomeView(FilterMixin, ListView):
    model = Post
    context_object_name = 'posts'    
    template_name = "posts/browse.html"

    def dispatch(self, request, *args, **kwargs):
        # Redirect to wst homepage
        if not request.user.is_authenticated() and request.path == "/":
            return render(request, 'home.html', {})
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)
       

    def get_queryset(self):
        qs = super(HomeView, self).get_queryset()
        
        # Filter by subscriptions
        user = self.request.user
        subscribed_to = []
        if user.is_authenticated():
            subscribed_to = self.request.user.subscribed_to.all()
        
        qs = [p for p in qs if (p.author in subscribed_to) or (p.author == user)]

        sorting = self.request.GET.get('sorting')
        if not sorting:
            qs = sorted(qs, key=lambda x: x.pub_date, reverse=True)
        
        
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['form'] = PostForm()
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

        sorting = self.request.GET.get('sorting')
        if not sorting:
            qs = sorted(qs, key=lambda x: x.pub_date, reverse=True)
        
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

        # Posttype
        posttype = self.request.GET.get('posttype')
        context['posttype'] = posttype
        

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
        context['hub'] = hub
        return context    
    


class HubList(ListView):
    model = Hub
    template_name = "hubs/hubs.html"




    


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
    notification = Notification(from_user=request.user,
                                to_user=post.author,
                                post=post,
                                notification_type="upvote")
    notification.save()
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
        
    replies = get_replies(post=post)

    # Footer info
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        subscribed_to = request.user.subscribed_to.all()
    else:
        upvoted = []
        subscribed_to = []

    # increment views counter. Do clever memcache laters.
    if not request.user.is_staff and request.user != post.author:
        post.views +=1
        post.save()

    # Just for private website subheader
    userprofile = post.author

    form = PostForm()
    hubs = Hub.objects.all()
    return render(request, 'posts/post.html',{
        'post': post,
        'upvoted': upvoted,
        'replies': replies,                
        'hubs':hubs,
        'form':form,
        'subscribed_to':subscribed_to,
        'userprofile':userprofile,        
    })

def post_create(request, parentslug=""):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.score += 1 # self upvote

            if parentslug:
                post.parent = Post.objects.get(slug=parentslug)

            post.save()

            # Notification
            if parentslug:
                notification = Notification(from_user=request.user,
                                            to_user=post.parent.author,
                                            post=post,
                                            notification_type="reply")
                notification.save()
                post.parent.author.new_notifications = True
                post.parent.author.save()
                
            
            request.user.upvoted.add(post)

            # Add hubs
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            
            if parentslug:
                return HttpResponseRedirect('/post/'+parentslug+"#"+post.slug)
            else:
                return HttpResponseRedirect('/') # story/'+post.slug+'/edit'
    else:
        form = PostForm()

    return render(request, 'posts/create.html', {
            'form':form,
            'hubs':Hub.objects.all(),
            'test': ""
        })



def repost(request, slug=""):
    original_post = Post.objects.get(slug=slug)
    post = Post()
    post.author = request.user
    post.repost= original_post
    post.save()

    # Notification
    notification = Notification(from_user=request.user,
                                to_user=original_post.author,
                                post=original_post,
                                notification_type="repost")
    notification.save()
    original_post.author.new_notifications = True
    original_post.author.save()
    
    return HttpResponseRedirect('/@'+post.author.username)


def post_edit(request, slug):
    post = Post.objects.get(slug=slug)
    # throw him out if he's not an author
    if request.user != post.author and not request.user.is_staff:
        return HttpResponseRedirect('/')        

    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save(slug=post.slug)                

            post.hubs = []
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            return HttpResponseRedirect('/post/'+post.slug)
    else:
        form = PostForm(instance=post)
        form.fields["hubs"].queryset = Hub.objects.all()

    return render(request, 'posts/edit.html', {
        'post':post,
        'form':form,
    })


def post_delete(request, slug):
    post = Post.objects.get(slug=slug)

    # throw him out if he's not an author
    if request.user != post.author:
        return HttpResponseRedirect('/')        

    post.delete()
    return HttpResponseRedirect('/')


    
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



    

