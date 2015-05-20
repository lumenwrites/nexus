from django.shortcuts import render

def index(request):
    return render(request, 'chaoslegion/posts.html',{
    })

def page(request):
    return render(request, 'chaoslegion/page.html',{
    })

def user(request):
    return render(request, 'chaoslegion/user.html',{
    })
