from django.shortcuts import render

from .models import Challenge

from stories.forms import StoryForm
from stories.models import Story
from hubs.models import Hub

def challenges(request):
    challenges = Challenge.objects.all().order_by('-pub_date')     
    return render(request, 'challenges/challenges.html', {
        'challenges': challenges,
    })

def challenge(request, slug):
    challenge = Challenge.objects.get(slug=slug)
    return render(request, 'challenges/challenge.html', {
        'challenge': challenge,
    })

def submissions(request, slug):
    challenge = Challenge.objects.get(slug=slug)
    return render(request, 'stories/stories.html', {
        'challenge': challenge,
    })

def results(request, slug):
    challenge = Challenge.objects.get(slug=slug)
    return render(request, 'challenges/challenge.html', {
        'challenge': challenge,
    })

def story_submit(request, slug):
    challenge = Challenge.objects.get(slug=slug)    
    if request.method == 'POST':
        form = StoryForm(request.POST)
        if form.is_valid():
            story = form.save(commit=False) # return story but don't save it to db just yet
            story.challenge = challenge
            story.author = request.user
            # self upvote
            story.score += 1
            story.save()
            request.user.upvoted.add(story)            
            story.hubs.add(*form.cleaned_data['hubs'])
            hubs = story.hubs.all()
            for hub in hubs:
                if hub.parent:
                    story.hubs.add(hub.parent)
            # Hacky way to 
            # for hub in form.cleaned_data['hubs']:
            #     if hub.parent:
            #         story.hubs.add(hub.parent)
            #         if hub.parent.parent:
            #             story.hubs.add(hub.parent.parent)
            return HttpResponseRedirect('/story/'+story.slug+'/edit')
    else:
        form = StoryForm()
        form.fields["hubs"].queryset = Hub.objects.filter(children=None).order_by('id')

    return render(request, 'stories/story-create.html', {
        'form':form,
        'hubs':Hub.objects.all()
    })
