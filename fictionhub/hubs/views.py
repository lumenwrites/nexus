import re # praw

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# for 404
from django.shortcuts import render_to_response
from django.template import RequestContext

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
