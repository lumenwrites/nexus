from django.conf.urls import url

from . import views
from stories.views import stories as stories
urlpatterns = [
    url(r'^challenges/$', views.challenges),

    url(r'^challenge/(?P<slug>[^\.]+)/submit-story$', views.story_submit),

    url(r'^challenge/(?P<challenge>[^\.]+)/submissions$', stories,
        {'filterby': 'challenge'}),    
    
    url(r'^challenge/(?P<slug>[^\.]+)/results$', views.results),        

    url(r'^challenge/(?P<slug>[^\.]+)$', views.challenge, name='view_challenge'),
    
]
