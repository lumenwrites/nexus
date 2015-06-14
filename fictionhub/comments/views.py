# Standard library
import datetime, re # praw
from django.utils.timezone import utc

# Core django components
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext

# My own stuff
# Forms
from posts.forms import PostForm
from hubs.forms import HubForm
from comments.forms import CommentForm
# Models
from profiles.models import User
from hubs.models import Hub
from posts.models import Post
from comments.models import Comment


def comment_submit(request, comment_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent = Comment.objects.get(id=comment_id)
            comment.post = comment.parent.post
            comment.save()
            comment_url = request.GET.get('next', '/')+"#id-"+str(comment.id)
            return HttpResponseRedirect(comment_url)
        else:
            # return HttpResponse("string")
            return render(request, 'posts/create.html', {
                'form':form,
            })


def comment_edit(request, comment_id):
    comment = Comment.objects.get(id = comment_id)
    nextpage = request.GET.get('next', '/')

    if request.method == 'POST':
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.save()
            return HttpResponseRedirect(nextpage)
    else:
        form = CommentForm(instance=comment)
    
    return render(request, 'comments/comment-edit.html', {
        'comment':comment,
        'form':form,
        'nextpage':nextpage
    })
    
    # throw him out if he's not an author
    if request.user != comment.author:
        return HttpResponseRedirect('/')        
    return HttpResponseRedirect('/') # to story list

        
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id = comment_id)

    # throw him out if he's not an author
    if request.user != comment.author:
        return HttpResponseRedirect('/')        
    try:
        path = '/story/'+comment.parent.post.slug + '/' + comment.post.slug + '#comments'
    except:
        path = '/story/'+comment.post.slug + '#comments'

    comment.delete()

    return HttpResponseRedirect(path) # to story list

        
# Comment voting
# Voting
def comment_upvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score += 1
    comment.save()
    comment.author.karma += 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.add(comment)
    user.save()
    return HttpResponse()

def comment_downvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    if comment.score > 0:
        comment.score -= 1
        comment.author.karma -= 1        
    comment.save()
    comment.author.save()
    user = request.user
    user.comments_downvoted.add(comment)
    user.save()
    return HttpResponse()

def comment_unupvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score -= 1
    comment.save()
    comment.author.karma = 1
    comment.author.save()
    user = request.user
    user.comments_upvoted.remove(comment)
    user.save()
    return HttpResponse()

def comment_undownvote(request):
    comment = Comment.objects.get(id=request.POST.get('comment-id'))
    comment.score += 1
    comment.author.karma += 1        
    comment.save()
    comment.author.save()
    user = request.user
    user.comments_downvoted.remove(comment)
    user.save()
    return HttpResponse()

def comments_user(request, username, filterby="", comment_id=""):
    # wtf, is it just copypaste from comments list?
    # comments user has no submit form
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

    userprofile = User.objects.get(username=username)
    top_lvl_comments = Comment.objects.filter(author = userprofile)

    rankby = "new"
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
    # comments = list(get_comment_list(ranked_comments, rankby=rankby))
    comments = ranked_comments

    if request.user.is_authenticated():
        comments_upvoted = request.user.comments_upvoted.all()
        comments_downvoted = request.user.comments_downvoted.all()                
        subscribed_to = request.user.subscribed_to.all()
    else:
        comments_upvoted = []
        comments_downvoted = []  
        subscribed_to = []
    
    filterurl = '/user/'+ userprofile.username
    return render(request, 'comments/comments-user.html',{
        'upvoted': upvoted,
        'downvoted': downvoted,
        'comments_upvoted': comments_upvoted,
        'comments_downvoted': comments_downvoted,
        'comments': comments,
        'form': form,
        'subscribed_to':subscribed_to,
        'filterby':'comments_user',
        'userprofile':userprofile,
        'filterurl':filterurl
    })
