from django.shortcuts import render

def challenges(request):
    return render(request, 'challenges/challenges.html')
