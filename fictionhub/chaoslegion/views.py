import datetime
from django.utils.timezone import utc

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import PostForm


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
    # if category_slug: # filter by hub
    #     category_id = Category.objects.get(slug=category_slug).id
    #     posts = posts.filter(category=category_id)
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
    else:
        upvoted = []
    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'rankby': "hot"
    })

# View new posts
def new_posts(request):
    posts = Post.objects.all().order_by('-pub_date')#[:consider]

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
    else:
        upvoted = []

    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted,
        'rankby': "new"        
    })

# View top posts
def top_posts(request,slug):
    posts = rank_top_posts(timespan = slug)

    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
    else:
        upvoted = []

    return render(request, 'chaoslegion/posts.html',{
        'posts' : posts,
        'user': request.user,
        'upvoted': upvoted,
        'rankby':slug,
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
    return render(request, 'chaoslegion/post.html',{
        'post': get_object_or_404(Post, slug=slug)
    })
    

# Voting
def upvote(request):
    post = get_object_or_404(Post, id=request.POST.get('post-id'))
    post.score += 1
    post.save()
    user = request.user
    user.upvoted.add(post)
    user.save()
    return HttpResponse()


def downvote(request):
    pass




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

def user(request):
    return render(request, 'chaoslegion/user.html',{
    })

def about(request):
    return render(request, 'chaoslegion/about.html',{
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
