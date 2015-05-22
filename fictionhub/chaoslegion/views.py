from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from .forms import PostForm

def posts(request):
    posts = Post.objects.all()
    if request.user.is_authenticated():
        upvoted = request.user.upvoted.all()
    else:
        upvoted = []
    return render(request, 'chaoslegion/posts.html',{
        'posts': posts,
        'user': request.user,
        'upvoted': upvoted
    })

def post(request, slug):
    return render(request, 'chaoslegion/post.html',{
        'post': get_object_or_404(Post, slug=slug)
    })


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
