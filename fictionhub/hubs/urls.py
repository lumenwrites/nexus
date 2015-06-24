from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hubs/$', views.hubs),        
    url(r'^hub/add/$', views.hub_create),    
]
