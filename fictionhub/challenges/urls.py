from django.conf.urls import url

from . import views
from .views import PromptCreate

urlpatterns = [
    # url(r'^hubs/$', views.hubs),        
    # url(r'^hub/add/$', views.hub_create),
    url(r'^prompt/add/$', PromptCreate.as_view()),        
]
