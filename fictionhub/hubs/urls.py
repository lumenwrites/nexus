from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hub/add/$', views.hub_create),    
]
