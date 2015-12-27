from django.shortcuts import render

# Create your views here.

def quests(request):
    return render(request, 'posts/test.html', {})
