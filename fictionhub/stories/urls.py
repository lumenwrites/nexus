from django.conf.urls import url

from . import views

urlpatterns = [


    url(r'^story/add$', views.story_create),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/edit$', views.chapter_edit),    
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/up$', views.chapter_up),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/down$', views.chapter_down),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/delete$', views.chapter_delete),        
    
    url(r'^story/(?P<story>[^\.]+)/edit$', views.story_edit),
    url(r'^story/(?P<story>[^\.]+)/delete$', views.story_delete),      
    url(r'^story/(?P<story>[^\.]+)/add$', views.chapter_create),

    # View
    url(r'^user/(?P<username>[^\.]+)', views.user_stories),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)$', views.chapter),            
    url(r'^story/(?P<story>[^\.]+)', views.story, name='view_story'),    

    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),

    url(r'^(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.stories),    
    url(r'^(?P<rankby>[^\.]+)/$', views.stories),    
    url(r'^$', views.stories),
    # url(r'^story/(?P<story>[^\.]+)/feed$', views.story_feed),    
]
