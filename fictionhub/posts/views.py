# standard library imports
import re
from string import punctuation
# to round views
import math

# for rss
from xml.etree.ElementTree import Element, SubElement, tostring 
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse



import json # for temporary post api. Replace with REST.
import feedparser
from bs4 import BeautifulSoup # to parse prompt
from html2text import html2text
from django.db.models import Q

# core django components
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import * # for rss
from django.core.mail import send_mail # for email
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext
# date
from datetime import datetime
from django.utils.timezone import utc
from time import mktime
# slugify dropbox title
from django.template.defaultfilters import slugify
from django.conf import settings

# My own stuff
# utility functions
from comments.utils import get_comment_list
from .utils import rank_hot, rank_top, check_if_rational
from .ffnet import Munger, FFNetAdapter, FPAdapter
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



#dropbox
import os
import dropbox
from markdown import Markdown
import time

# wordpress
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost, GetPost
from wordpress_xmlrpc.methods.users import GetUserInfo


def posts(request, rankby="hot", timespan="all-time",
            filterby="", hubslug="", username="", challenge="",
          prompt=""):

    # for user profile navbar
    userprofile = []
    filterurl = ""
    post_type = "story"
    if not challenge:
        challenge = []
    if not prompt:
        prompt = []

    rational = check_if_rational(request)

    if not request.user.is_anonymous():
        subscribed_to = request.user.subscribed_to.all()
    else:
        subscribed_to = []
    
    if filterby == "subscriptions":
        subscribed_to = request.user.subscribed_to.all()
        posts = Post.objects.filter(author=subscribed_to, published=True)
        # posts = Post.objects.all()        
        filterurl="/subscriptions" # to add to href  in subnav
    elif filterby == "hub":
        hub = Hub.objects.get(slug=hubslug)
        # Show posts from all the children hubs? Don't know how to sort.
        # children = Hub.objects.filter(parent=hub)
        # hubs = []
        if hubslug == "wiki":
            posts = Post.objects.filter(hubs=hub, published=True,
                                        post_type = "wiki")
            post_type = "wiki"
        else:
            posts = Post.objects.filter(hubs=hub, published=True, post_type = "story") #  rational = rational, 
        filterurl="/hub/"+hubslug # to add to href  in subnav
    elif filterby == "user":
        userprofile = get_object_or_404(User, username=username)
        if request.user == userprofile:
            # If it's my profile - display all the posts, even unpublished.
            # fictionhub includes rational        
            if rational:
                posts = Post.objects.filter(author=userprofile,
                                            rational=rational).exclude(post_type="chapter")
            else:
                posts = Post.objects.filter(author=userprofile).exclude(post_type="chapter")
            # , post_type="story")
        else:
            # fictionhub includes rational        
            if rational:
                posts = Post.objects.filter(author=userprofile,
                                            rational=rational,
                                            published=True).exclude(post_type="chapter")
            else:
                posts = Post.objects.filter(author=userprofile,
                                            published=True)
        filterurl="/user/"+userprofile.username # to add to href  in subnav
    elif filterby == "challenges":
        posts = Post.objects.filter(post_type = "challenge", published=True, rational = rational)
        rankby = "new"
    elif filterby == "challenge":
        challenge = Post.objects.get(slug=challenge)
        if challenge.state == "voting":
            rankby = "new" # later do random
        elif challenge.state == "completed":            
            rankby = "top"
        posts = Post.objects.filter(parent=challenge, published=True, rational = rational)
    elif filterby == "prompt":
        prompt = Post.objects.get(slug=prompt)
        posts = Post.objects.filter(parent=prompt)#, published=True, rational = rational)
        rankby = "hot"
    else:
        # fictionhub includes rational        
        if rational:
            posts = Post.objects.filter(published=True, rational = rational, post_type="story")
        else:
            posts = Post.objects.filter(published=True, post_type="story")
        # fictionhub doesn't include rational
        # posts = Post.objects.filter(published=True, rational = rational, post_type="story")
        filterurl="/stories"

    if rankby == "hot":
        post_list = rank_hot(posts, top=32)
    elif rankby == "top":
        post_list = rank_top(posts, timespan = timespan)
    elif rankby == "new":
        post_list = posts.order_by('-pub_date')
    else:
        post_list = []


    # Pagination
    paginator = Paginator(post_list, settings.PAGINATION_NUMBER_OF_PAGES)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)    

    # Disable upvoted/downvoted
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        

    
    # if not posts:
    #     return HttpResponseRedirect('/404')

    hubs = Hub.objects.all().order_by('id')

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

    solohub = False
    hubtitle = ""
    if filterby == "hub":
        hubtitle = hub.title
        solohub = True


    view_count = 0
    score = 0        
    try:
        # try is for solo hub, remove try lateer
        for post in userprofile.posts.all():
            view_count += post.views
            score += post.score
    except:
        pass

    if view_count > 1000:
        view_count = str(math.floor(view_count/1000)) + "K"

        
    return render(request, 'posts/posts.html',{
        'posts':posts,
        'upvoted': upvoted,
        'downvoted': downvoted,
        'filterby':filterby,
        'filterurl': filterurl,
        'hubslug': hubslug,        
        'post_type':post_type,
        'rankby': rankby,
        'timespan': timespan,
        'userprofile':userprofile,
        'subscribed_to': subscribed_to,
        'hubs': hubs,
        'challenge':challenge,
        'prompt':prompt,
        'solohub':solohub,
        'hubtitle':hubtitle,
        'view_count':view_count,
        'score':score,
    })



def browse(request, rankby="hot", timespan="all-time"):
    rational = check_if_rational(request)


    post_type = "story"

    query = ""
    selectedhubs = ""
    filterhubs = []
    if request.method == 'GET':
        # selectedhubs = request.GET.getlist('hubs')
        try:
            selectedhubs = request.GET['hubs'].split(",")
        except:
            electedhubs = []
        filterhubs = []
        if selectedhubs:
            for hubslug in selectedhubs:
                filterhubs.append(Hub.objects.get(slug=hubslug))
            if hubslug == "wiki":
                post_type = "wiki"                
                
            # Both
            posts = Post.objects.all()
            for hub in filterhubs:
                posts = posts.filter(hubs=hub)
        else:
            posts = Post.objects.all()            

        # Approved only
        posts = posts.filter(author__approved=True)

        query = request.GET.get('query')
        if query:
            # fictionhub includes rational
            if rational:
                posts = posts.filter(Q(title__icontains=query,
                                       published=True, post_type=post_type,
                                       rational = rational) |
                                     Q(body__icontains=query,
                                       published=True, post_type=post_type,
                                       rational = rational) |
                                     Q(author__username__icontains=query,
                                       published=True, post_type=post_type,
                                       rational = rational))
            else:
                posts = posts.filter(Q(title__icontains=query,
                                       published=True, post_type=post_type) |
                                     Q(body__icontains=query,
                                       published=True, post_type=post_type) |
                                     Q(author__username__icontains=query,
                                       published=True, post_type=post_type))
        else:
            # fictionhub includes rational            
            if rational:
                posts = posts.filter(published=True, rational = rational, post_type=post_type)
            else:
                posts = posts.filter(published=True, post_type=post_type)
            
    else:
        # fictionhub includes rational        
        if rational:
            posts = Post.objects.filter(published=True, rational = rational, post_type=post_type)
        else:
            posts = Post.objects.filter(published=True,post_type=post_type)
        
        filterhubs = []


    # Ranking
    if rankby == "hot":
        post_list = rank_hot(posts, top=32)
    elif rankby == "top":
        post_list = rank_top(posts, timespan = timespan)
    elif rankby == "new":
        post_list = posts.order_by('-pub_date')
    else:
        post_list = []


    # Pagination
    paginator = Paginator(post_list, settings.PAGINATION_NUMBER_OF_PAGES)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)    

    hubs = Hub.objects.all().order_by('id')

    # Disable upvoted/downvoted
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        

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

    if not query:
        query = ""

    solohub = False
    # if len(filterhubs) == 1:
    #     solohub=True
    return render(request, 'posts/browse.html',{
        'posts':posts,
        'rankby': rankby,
        'filterurl': "/browse",
        'upvoted': upvoted,
        'downvoted': downvoted,
        'timespan': timespan,
        'query':query,
        'hubs': hubs,
        'filterhubs':filterhubs,
        'solohub':solohub,
        'test': request.POST
    })


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



def post(request, story, comment_id="", chapter="", rankby="new", filterby=""):
    if request.path[-1] == '/':
        return redirect(request.path[:-1])

    try:
        story = Post.objects.get(slug=story)
    except:
        return HttpResponseRedirect('/404')
        

    try:
        # doesn't work if 2 chapters #1
        first_chapter = Post.objects.get(parent=story, number=1)
        # first_chapter = story.children.filter(number=1)[0]
    except:
        first_chapter = []
    

    # If chapter
    if chapter:
        chapter = Post.objects.get(parent=story,slug=chapter)
        first_chapter = []  # empty first chapter to show the right button in post template
        try:
            prev_chapter = Post.objects.get(parent=story, number=chapter.number-1)
        except:
            prev_chapter = []

        try:
            next_chapter = Post.objects.get(parent=story, number=chapter.number+1)
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
            comment = form.save(commit=False) # return post but don't save it to db just yet
            comment.author = request.user
            comment.parent = None
            if chapter:
                comment.post = chapter                
            else:
                comment.post = story
            comment.save()
            # Send Email
            # if comment.post.author.email_comments:
            #     commentauthor = comment.author.username
            #     topic = commentauthor + " has commented on your story "
            #     body = commentauthor + " has left a comment on your story\n" +\
            #            "http://fictionhub.io"+comment.post.get_absolute_url()+ "\n" +\
            #            "'" + comment.body[:64] + "...'"
            #     body += "\n\nYou can manage your email notifications in preferences:\n" +\
            #             "http://fictionhub.io/preferences/"
            #     try:
            #         email = comment.post.author.email            
            #         send_mail(topic, body, 'raymestalez@gmail.com', [email], fail_silently=False)
            #     except:
            #         pass
            # Notification
            message = Message(from_user=request.user,
                              to_user=comment.post.author,
                              story=comment.post,
                              comment=comment,
                              message_type="comment")
            message.save()
            comment.post.author.new_notifications = True
            comment.post.author.save()
            

            if comment.comment_type == "comment":
                if chapter:
                    return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'#comments')
                else:
                    return HttpResponseRedirect('/story/'+story.slug+'#comments')
            else:
                if chapter:
                    return HttpResponseRedirect('/story/'+story.slug+'/'+chapter.slug+'/reviews#comments')
                else:
                    return HttpResponseRedirect('/story/'+story.slug+'/reviews#comments')
                
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
    if filterby == "reviews":
        filterurl = "reviews"
        if chapter:
            top_lvl_comments = Comment.objects.filter(post = chapter,
                                                      comment_type="review",
                                                      parent = None)
        else:
            top_lvl_comments = Comment.objects.filter(post = story,
                                                      comment_type="review",
                                                      parent = None)
    else:
        if chapter:
            top_lvl_comments = Comment.objects.filter(post = chapter,
                                                      comment_type="comment",
                                                      parent = None)
        else:
            top_lvl_comments = Comment.objects.filter(post = story,
                                                      comment_type="comment",
                                                      parent = None)

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

    if chapter:
        post = chapter
    else:
        post = story

    if filterby:
        filterby = "/" + filterby
    else:
        filterby = "/comments"

    # Increment views counter. Do clever memcache laters.
    if not request.user.is_staff and request.user != post.author:
        post.views +=1
        post.save()

    # Count words
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
    post.wordcount = wordcount

    # orangemind
    orangemind = False
    # if request.META['HTTP_HOST'] == "orangemind.io":
        # orangemind = True
        
    return render(request, 'posts/post.html',{
        'post': post,
        'first_chapter':first_chapter,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,       
        'upvoted': upvoted,
        'downvoted': downvoted,
        'comments': comments,
        'comments_upvoted': comments_upvoted,
        'comments_downvoted': comments_downvoted,
        'rankby': rankby,        
        'form': form,
        'hubs':hubs,
        'subscribed_to':subscribed_to,
        'filterby':filterby,
        'orangemind':orangemind
    })

def post_create(request, story="", challenge="", prompt="", posttype="", hubslug=""):
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True
    
    if request.method == 'POST':
        form = PostForm(request.POST, storyslug=story)
        if form.is_valid():
            post = form.save(commit=False) # return post but don't save it to db just yet
            post.author = request.user
            # self upvote
            post.score += 1
            post.post_type = "story"
            post.rational = rational
            if story:
                post.parent = Post.objects.get(slug=story)
                post.post_type = "chapter"
                number_of_chapters = post.parent.children.count()
                post.number = number_of_chapters + 1
            if challenge:
                post.parent = Post.objects.get(slug=challenge)
            if prompt:
                post.parent = Post.objects.get(slug=prompt)
            if posttype == "post":
                post.post_type = "post"                    
            if posttype == "thread":
                post.post_type = "post"
            post.save()
            request.user.upvoted.add(post)            
            post.hubs.add(*form.cleaned_data['hubs'])
            hubs = post.hubs.all()
            if posttype == "thread":
                post.hubs.add(Hub.objects.get(slug=hubslug))
            for hub in hubs:
                if hub.parent and hub.parent.hub_type != "folder":
                    post.hubs.add(hub.parent)
                    if hub.parent.parent and hub.parent.parent.hub_type != "folder":
                        post.hubs.add(hub.parent.parent)

            # Hacky way to 
            # for hub in form.cleaned_data['hubs']:
            #     if hub.parent:
            #         post.hubs.add(hub.parent)
            #         if hub.parent.parent:
            #             post.hubs.add(hub.parent.parent)
            if story:
                return HttpResponseRedirect('/story/'+post.parent.slug+'/'+post.slug+'/edit')
            elif posttype == "post":
                return HttpResponseRedirect('/post/'+post.slug+'/edit')
            else:
                return HttpResponseRedirect('/story/'+post.slug+'/edit')
    else:
        form = PostForm()
        form.fields["hubs"].queryset = Hub.objects.filter(hub_type="hub")
        # Hub.objects.filter(children=None).order_by('id')
        if challenge:
            challenge = Post.objects.get(slug=challenge)
        else:
            challenge =[]
        if prompt:
            prompt = Post.objects.get(slug=prompt)
        else:
            prompt =[]            

    if story:
        story = Post.objects.get(slug=story)
        return render(request, 'posts/edit.html', {
            'story':story,        
            'form':form,
            'action':'chapter_create',
            'challenge':challenge,
            'posttype':posttype,
            'hubslug':hubslug,                        
            'prompt':prompt            
        })
    else:
        return render(request, 'posts/create.html', {
            'form':form,
            'hubs':Hub.objects.all(),
            'challenge':challenge,
            'prompt':prompt,
            'posttype':posttype,
            'hubslug':hubslug,                                    
            'test': ""
        })


def post_edit(request, story, chapter=""):
    story = Post.objects.get(slug=story)
    action = "story_edit"
    if chapter:
        chapter = Post.objects.get(parent=story,slug=chapter)
        action="chapter_edit"

    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

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
            if chapter:
                post.post_type = "chapter"
                post.parent = story
            post.save()
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

    if story.post_type == "wiki" or story.post_type == "post":
        return render(request, 'posts/edit-post.html', {
            'story':story,
            'chapter':chapter,            
            'form':form,
            'action':action
        })
    else:
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




def page_404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


class MainFeed(Feed):
    title = "fictionhub"
    link = "/feed/"
    description = "fictionhub"

    def items(self):
        return Post.objects.filter(published=True,post_type="story").order_by('-pub_date')[:25]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        md = Markdown()
        return md.convert(item.body)

    # item_link is only needed if NewsItem has no get_absolute_url method.
    def item_link(self, item):
        return item.get_absolute_url()
    
def post_feed(request, story):
    story = Post.objects.get(slug=story)
    rss = Element('rss')
    rss.set("version","2.0")

    channel = SubElement(rss,'channel')

    title = SubElement(channel,'title')
    title.text = story.title

    link = SubElement(channel,'link')
    link.text = "/story/"+story.slug # request.build_absolute_uri(reverse("post"))

    desc = SubElement(channel,'description')
    desc.text = story.body

    chapters = story.children.all()

    for index in chapters:
        item = SubElement(channel,'item')

        title_c = SubElement(item,'title')
        title_c.text = index.title
        
        link = SubElement(item,'link')
        #link.text = request.build_absolute_uri(index.get_absolute_url())
        link.text = "/story/"+story.slug
    return HttpResponse(tostring(rss, encoding='UTF-8'), content_type='application/xml')




def age(timestamp):
    now = datetime.utcnow().replace(tzinfo=utc)
    created_at = datetime.fromtimestamp(timestamp).replace(tzinfo=utc)
    
    age_in_minutes = int((now-created_at).total_seconds())/60

    # usage: age(prompt.created_utc)
    return age_in_minutes


    
    
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


def users(request):
    users = User.objects.all().order_by('-karma')[:100]
    return render(request, 'profiles/users.html',{
        'users':users,
        'hubs': [],        
    })

    


# rss
# rss
class UserFeed(Feed):
    title = "fictionhub latests stories"
    link = "/"
    feed_type = Atom1Feed

    def get_object(self, request, username):
        return get_object_or_404(User, username=username)

    def title(self, obj):
        return "fictionhub: %s latest stories" % obj.username

    def link(self, obj):
        return "http://fictionhub.io/user/" + obj.username
        # return "http://fictionhub.io/" +  str(item.get_absolute_url())
    
    def items(self, obj):
        return Post.objects.filter(published=True, author=obj).order_by("-pub_date")

    def item_title(self, item):
        return item.title
    
    def item_pubdate(self, item):
        return item.pub_date

    def item_description(self, item):
        md = Markdown()
        return md.convert(item.body)



    
# TODO: replace with CBVs
# from django.views.generic import View,TemplateView, ListView, DetailView, FormView, CreateView
# from django.shortcuts import render

# from .models import Post
# from .forms import PostForm
# from .utils import rank_hot, rank_top



# class PostsView(ListView):
#     model = Post
#     template_name = "posts/posts.html"

#     def get_queryset(self):
#         posts = Post.objects.all()

#         rankby = self.kwargs['rankby']
#         if rankby == "hot":
#             post_list = rank_hot(posts, top=32)
#         elif rankby == "top":
#             post_list = rank_top(posts, timespan = timespan)
#         elif rankby == "new":
#             post_list = posts.order_by('-pub_date')
#         else:
#             post_list = []

#         return posts

#     def get_context_data(self, **kwargs):
#         context = super(PostsView, self).get_context_data(**kwargs)
#         context['rankby'] =  self.kwargs['rankby']
#         return context    
        

# class PostView(DetailView):
#     model = Post
#     template_name = "posts/post.html"    

# class PostCreate(CreateView):
#     model = Post
#     form_class = PostForm
#     template_name = "posts/create.html"    

# class PostEdit(FormView):
#     template_name = "posts/edit.html"    
#     form_class = PostForm

#     success_url = '/thanks/'

#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.send_email()
#         return super(ContactView, self).form_valid(form)    

# TODO: dry it in one function
# def vote(request):
#     post = Post.objects.get(id=request.POST.get('post-id'))
#     vote =  request.POST.get('vote')
#     user = request.user

#     if post in user.upvoted:    # unupvote
#         post.score -= 1
#         post.author.karma -= 1
#         user.upvoted.remove(post)
#     elif post in user.downvoted:# undownvote
#         post.score += 1
#         post.author.karma += 1
#         user.downvoted.remove(post)
#     elif vote == "up":          # upvote
#         post.score += 1
#         post.author.karma += 1
#         user.upvoted.add(post)
#     elif vote == "down":        # downvote
#         if post.score > 0:
#             post.score -= 1
#             post.author.karma -= 1
#             user.downvoted.add(post)

#     post.save()
#     post.author.save()
#     user.save()

#     return HttpResponse()




from django.views.generic.list import ListView

class HubList(ListView):
    model = Hub
    template_name = "hubs/hubs.html"


class SeriesList(ListView):
    model = Post
    template_name = "series/series.html"
    paginate_by=15
    

    

import praw    

    # prompts
def writing_prompts(request):
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
        and ((prompt.num_comments-2) < 2) \
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

            prompts.append(prompt)
                


    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)
            
        
    return render(request, 'posts/writing-prompts.html', {
        'prompts': prompts[:16],
        'max_age': max_age,        
    })



# Editorial
def prompt(request):
    r = praw.Reddit(user_agent='Request new prompts from /r/writingprompts by /u/raymestalez')
    subreddit = r.get_subreddit('writingprompts')
    prompts = subreddit.get_new(limit=64)
    new_prompts = list(prompts)
    prompts = []

    # less than 5 replies, more than 1 upvote and less than 60 minutes old
    for prompt in new_prompts:
        if (prompt.score > 1) \
        and ((prompt.num_comments-2) < 4) \
        and (age(prompt.created_utc) < 5*60):
            if prompt.num_comments > 0:
                prompt.num_comments -= 2 # remove 2 fake replies
            prompts.append(prompt)

    # sort by score
    prompts.sort(key=lambda p: p.score, reverse=True)

    prompt = prompts[0]

    promptslist = ["\n\n" + p.title for p in prompts]
    return HttpResponse(promptslist) #prompt.title
    

    
def prompts_repost(request):
    print ("\n\n################ Log ################") 
    print (time.strftime("%d/%m/%Y"))
    print(time.strftime("%H:%M:%S"))
    print ("################")
    
    # Dropbox
    access_token = os.environ["ACCESS_TOKEN"]
    client = dropbox.client.DropboxClient(access_token)
    folder_metadata = client.metadata('/prompts/')
    
    teststring = "\n\n"
    imported = ""
    updated = ""
    
    for file in folder_metadata["contents"]:
        if not file["is_dir"]:
            path = file["path"]
            f, metadata = client.get_file_and_metadata(path)
            text = f.read()
            text = text.decode("utf-8")
    
            md = Markdown(extensions = ['meta', 'codehilite'])
            content = md.convert(text)
            metadata = {}
            for name, value in md.Meta.items():
                metadata[name] = value[0]
                # teststring += name + ": " + value[0] + "<br/>"
    
            # teststring += "Title: " + metadata['title'] + "\n" + \
            #               "Date: " + metadata['date'] + \
            #               "Content: " + content
    
            publish = False
            try:
                if metadata['publish'].strip() == "True":
                    publish = True
            except:
                pass
                    
    
            if publish:
                # Reddit
                r = praw.Reddit(user_agent='Auto submit prompt replies from dropbox by /u/raymestalez')
                r.login(os.environ["REDDITUNAME"],os.environ["REDDITUPASS"])
                subreddit = r.get_subreddit('WritingPrompts')
                
                title = metadata["prompt"].strip()
                # print("Title: " + title)
                
                # remove meta from text
                text = "".join(text.split("\n\n", 1)[1:]).strip()
                body = text
    
                # Get or create prompt            
                thread = list(r.search(title, subreddit=subreddit, sort="new")) #, syntax='cloudsearch'
                if thread:
                    thread = thread[0]
                    teststring += "Thread selected " + title + "\n"
                # else:
                #     thread = r.submit('/r/WritingPrompts', title, text=' ')
                #     print("Thread created " + title)
    

                edited = False
                comments = praw.helpers.flatten_tree(thread.comments)
                for comment in comments:
                    try:
                        if comment.author.name == "raymestalez":
                            comment.edit(body)
                            print ("################")
                            edited = True
                            teststring += "Prompt Edited " + body[:10] + "\n"
                    except:
                        pass
                        
                if not edited:
                    thread.add_comment(body)
                    print ("################")
                    teststring += "Prompt Submitted  " + body[:10]

    return render(request, 'posts/test.html', {
        'teststring': teststring,
    })


