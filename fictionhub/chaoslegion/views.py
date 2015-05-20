from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import PostForm

def posts(request):
    posts = Post.objects.all()
    return render(request, 'chaoslegion/posts.html',{
        'posts': posts
    })

def index(request):
    return render(request, 'chaoslegion/posts.html',{
    })

def post(request, slug):
    return render(request, 'chaoslegion/post.html',{
        'post': get_object_or_404(Post, slug=slug)
    })

@login_required
def submit(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PostForm()
    return render(request, 'chaoslegion/submit.html', {'form':form})

def user(request):
    return render(request, 'chaoslegion/user.html',{
    })
