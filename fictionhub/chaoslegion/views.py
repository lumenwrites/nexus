import datetime
from django.utils.timezone import utc
import re
import praw

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import PostForm, CommentForm


def rank_hot_posts(top=180, consider=1000, hub_slug=None):
    def score(post, gravity=1.8, timebase=120):
        # number_of_comments = len(post.comments.all())
        rating = (post.score + 1)**0.8 # + number_of_comments
        now = datetime.datetime.utcnow().replace(tzinfo=utc)
        age = int((now - post.pub_date).total_seconds())/60
        return rating/(age+timebase)**1.8

    # top - number of stories to show,
    # consider - number of latest stories to rank
    posts = Post.objects.all()

    # filter by hub
    # if hub_slug: 
    #     hub = Hub.objects.get(slug=hub_slug)
    #     posts_in_hub = []
    #     for post in posts:
    #         if hub in post.hubs.all():
    #             posts_in_hub.append(post)
    #     posts = posts_in_hub

    latest_posts = posts.order_by('-pub_date')#[:consider]
    #comprehension, posts with rating, sorted
    posts_with_rating = [(score(post), post) for post in latest_posts]
    ranked_posts = sorted(posts_with_rating, reverse = True)
    #strip away the rating and return only posts
    return [post for _, post in ranked_posts][:top]

def rank_top_posts(timespan = None):
    posts = Post.objects.all()

    if timespan == "day":
        day = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('day')
        posts = posts.filter(pub_date__day = day)        
    elif timespan == "month":
        month = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('month')
        posts = posts.filter(pub_date__month = month)        
    elif timespan == "all-time":
        year = datetime.datetime.utcnow().replace(tzinfo=utc).__getattribute__('year')
        posts = posts.filter(pub_date__year = year)                
    
    top_posts = posts.order_by('-score')
    return top_posts

    
# View hot posts (main page)
def hot_posts(request):
    # posts = Post.objects.all()
    posts = rank_hot_posts(top=32)

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        
        
    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'downvoted': downvoted,                
        'rankby': "hot"
    })

# View new posts
def new_posts(request):
    posts = Post.objects.all().order_by('-pub_date')#[:consider]

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()        
    else:
        upvoted = []
        downvoted = []        

    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'downvoted': downvoted,        
        'rankby': "new"        
    })

# View top posts
def top_posts(request,slug):
    posts = rank_top_posts(timespan = slug)

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []                


    return render(request, 'chaoslegion/posts.html',{
        'posts' : posts,
        'user': request.user,
        'upvoted': upvoted,
        'downvoted': downvoted,                        
        'rankby':slug,
    })

# Hubs
def hub_new(request,slug):
    posts = Post.objects.all().order_by('-pub_date')#[:consider]

    # filter by hub
    hub = Hub.objects.get(slug=slug)
    posts_in_hub = []
    for post in posts:
        if hub in post.hubs.all():
            posts_in_hub.append(post)
    posts = posts_in_hub

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()        
    else:
        upvoted = []
        downvoted = []        

    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'downvoted': downvoted,        
        'rankby': "new"        
    })

# Subscriptions
def subscriptions(request):
    subscribed_to = request.user.subscribed_to.all()
    # posts = Post.objects.filter(author=subscriptions).order_by('-pub_date')#[:consider]
    all_posts = Post.objects.all().order_by('-pub_date')

    posts = []
    
    for post in all_posts:
        if post.author in subscribed_to:
            posts.append(post)

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()        
    else:
        upvoted = []
        downvoted = []        

    return render(request, 'chaoslegion/subscriptions.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'downvoted': downvoted,        
        'rankby': "new"        
    })

# View Hub
# def view_category(request,slug):
#     posts = top_posts(top=32, category_slug = slug)

#     if request.user.is_authenticated():
#         liked_posts = request.user.liked_posts.filter(id__in=[post.id for post in posts])
#     else:
#         liked_posts = []

#     categories = Category.objects.all()
#     return render(request, 'forum/forum.html',{
#         'posts' : posts,
#         'liked_posts':liked_posts,
#         'categories':categories,
#         'categoryTitle': Category.objects.get(slug=slug).title,
#         'currentCategory': Category.objects.get(slug=slug),
#     })    


# View one post
def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post = post)                

    hubs = post.hubs.all()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) # return story but don't save it to db just yet
            comment.author = request.user
            comment.parent = None
            comment.post = post
            comment.save()
            return HttpResponseRedirect('/post/'+slug+'#comments')
    else:
        form = CommentForm()
    
    
    return render(request, 'chaoslegion/post.html',{
        'post': post,
        'comments': comments,        
        'form': form,
        'hubs':hubs
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
    return HttpResponse()

def downvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    if post.score > 0:
        post.score -= 1
        post.author.karma -= 1        
    post.save()
    post.author.save()
    user = request.user
    user.downvoted.add(post)
    user.save()
    return HttpResponse()




# Submit post
@login_required
def submit(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # return story but don't save it to db just yet
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'chaoslegion/submit.html', {'form':form})

# Writing Prompt
@login_required
def prompt(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False) # return story but don't save it to db just yet
            post.author = request.user
            post.hubs = Hub.objects.get(slug="writing-prompts")
            post.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()

    r = praw.Reddit(user_agent='my_cool_application')
    prompts = (r.get_subreddit('WritingPrompts').get_new(limit=1))
    prompt = list(prompts)[0]
    promptstring = str(prompt.title)
    cleanprompt = re.sub('\[(.*?)\]', '', promptstring) # remove [WP]
    
    return render(request, 'chaoslegion/prompt.html', {
        'form':form,
        'prompt': cleanprompt
    })


# User
def user_new(request, username):
    userprofile = get_object_or_404(User, username=username)    
    posts = Post.objects.filter(author=userprofile).order_by('-pub_date')
    subscribed_to = request.user.subscribed_to.all()    

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
        downvoted = request.user.downvoted.all()                
    else:
        upvoted = []
        downvoted = []        
    
    return render(request, 'chaoslegion/user.html',{
        'posts':posts,
        'upvoted': upvoted,
        'downvoted': downvoted,                
        'userprofile':userprofile,
        'subscribed_to': subscribed_to
    })

def subscribe(request, username):
    userprofile = User.objects.get(username=username)    
    user = request.user
    user.subscribed_to.add(userprofile)
    user.save()
    return HttpResponseRedirect('/user/'+username)

def unsubscribe(request, username):
    userprofile = User.objects.get(username=username)    
    user = request.user
    user.subscribed_to.remove(userprofile)
    user.save()
    return HttpResponseRedirect('/user/'+username)


def about(request, username):
    userprofile = get_object_or_404(User, username=username)    
    posts = Post.objects.filter(author=userprofile).order_by('-pub_date')

    if request.method == 'POST':
        user = request.user
        userprofile.subscribers = user
        userprofile.save()
        return HttpResponseRedirect('/user/'+username)
    else:
        form = CommentForm()
    
    return render(request, 'chaoslegion/about.html',{
        'posts':posts,
        'userprofile':userprofile
    })


# Login or sign up
def login_or_signup(request):
    # If already logged in - get out of here
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    authenticate_form = AuthenticationForm(None, request.POST or None)
    register_form = UserCreationForm()    
    return render(request, "auth/login.html", {
        'authenticate_form': authenticate_form,
        'register_form': register_form,        
    })


# Only log in
def authenticate_user(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
 
    # Initialize the form either fresh or with the appropriate POST data as the instance
    auth_form = AuthenticationForm(None, request.POST or None)
 
    # Ye Olde next param so common in login.
    # I send them to their default profile view.
    nextpage = request.GET.get('next', '/')
 
    # The form itself handles authentication and checking to make sure passowrd and such are supplied.
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        return HttpResponseRedirect(nextpage)
 
    return render(request, 'auth/authenticate.html', {
        'form': auth_form,
        'title': 'User Login',
        'next': nextpage,
    })


# Only sign up
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # new_user = form.save()
            user = User.objects.create_user(form.cleaned_data['username'], None, form.cleaned_data['password1'])
            user.save()

            # log user in after signig up
            username = request.POST['username']
            password = request.POST['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "auth/register.html", {
        'form': form,
    })
