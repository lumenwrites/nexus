from django.conf.urls import url

from . import views

urlpatterns = [
    # Comments
    url(r'^comment-submit/(?P<comment_id>[^\.]+)', views.comment_submit),
    url(r'^comment-upvote/', views.comment_upvote),
    url(r'^comment-downvote/', views.comment_downvote),
    url(r'^comment-unupvote/', views.comment_unupvote),
    url(r'^comment-undownvote/', views.comment_undownvote),

    url(r'^comment/(?P<comment_id>[^\.]+)/edit', views.comment_edit),
    url(r'^comment/(?P<comment_id>[^\.]+)/delete', views.comment_delete), 
    
    # view comment
    url(r'^story/(?P<story>[^\.]+)/comment/(?P<comment_id>[^\.]+)', views.story),

    # Rank comments
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.story, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/comments/(?P<rankby>[^\.]+)$', views.story, name='view_story'),
]
