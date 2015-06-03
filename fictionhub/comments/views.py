import datetime, re # praw
from django.utils.timezone import utc

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import StoryForm, ChapterForm, CommentForm, HubForm
from .models import Story, Chapter, Hub, Comment
from profiles.models import User

from stories.views import rank_hot, rank_top

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

# Comments
def get_comment_list(comments=None, rankby="hot"):
    """Recursively build a list of comments."""
    yield 'in'

    # Loop through all the comments I've passed
    for comment in comments:
        # Add comment to the list
        yield comment
        # get comment's children
        children = comment.children.all()
        if rankby == "hot":
            ranked_children = rank_hot(children, top=32)
        elif rankby == "top":
            ranked_children = rank_top(children, timespan = "all-time")
        elif rankby == "new":
            ranked_children = children.order_by('-pub_date')
        else:
            ranked_children = []
        
        # If there's any children
        if len(ranked_children):
            comment.leaf=False
            # loop through children, and apply this function
            for x in get_comment_list(ranked_children, rankby=rankby):
                yield x
        else:
            comment.leaf=True
    yield 'out'

