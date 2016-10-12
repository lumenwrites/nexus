from django.conf.urls import url

from . import views
# from .views import HubCreate

urlpatterns = [
    url(r'^quests/$', views.quests),        
    # url(r'^hub/add/$', views.hub_create),
    # url(r'^hub/add/$', HubCreate.as_view()),        
]
