import re # praw

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext
# CBVs
from django.views.generic import CreateView
# Forms
from hubs.forms import HubForm

# Models
from profiles.models import User
from hubs.models import Hub


def hub_create(request):
    nextpage = request.GET.get('next', '/')
    
    if request.method == 'POST':
        form = HubForm(request.POST)
        if form.is_valid():
            hub = form.save(commit=False) # return story but don't save it to db just yet
            hub.save()
            return HttpResponseRedirect(nextpage)
    else:
        form = HubForm()

    return render(request, 'hubs/hub-create.html', {
        'form':form,
        'nextpage':nextpage
    })

class HubCreate(CreateView):
    model = Hub
    form_class = HubForm
    # nextpage = self.request.GET.get('next', '/')
    success_url="/"
    template_name = "hubs/hub-create.html"    



def hubs(request):
    rational = False
    if request.META['HTTP_HOST'] == "rationalfiction.io" or \
       request.META['HTTP_HOST'] == "localhost:8000":
        rational = True

    hubs = Hub.objects.all()

    return render(request, 'hubs/hubs.html', {
        'hubs':hubs
    })



def subscribe(request, slug):
    hub = Hub.objects.get(slug=slug)
    if not request.user.is_anonymous():
        user = request.user
        user.subscribed_to_hubs.add(hub)
        user.save()
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    else:
        return HttpResponseRedirect('/login/')    

def unsubscribe(request, slug):
    hub = Hub.objects.get(slug=slug)
    user = request.user
    user.subscribed_to_hubs.remove(hub)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
