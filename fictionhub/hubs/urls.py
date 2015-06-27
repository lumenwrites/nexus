from django.conf.urls import url

from . import views
from .views import HubCreate

urlpatterns = [
    url(r'^hubs/$', views.hubs),        
    # url(r'^hub/add/$', views.hub_create),
    url(r'^hub/add/$', HubCreate.as_view()),        
]
