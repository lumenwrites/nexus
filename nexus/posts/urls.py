from django.conf.urls import url
from django.views.generic import RedirectView


from . import views, feeds, repost
# from .feeds import MainFeed

urlpatterns = [

    # User Feed
    url(r'^user/(?P<username>[^\.]+)/feed/atom/$', feeds.UserFeed()),    

    # Store
    url(r'^user/rayalez/store/$', views.item),
    url(r'^book/$', views.book),


    # Class Based Views
    # Browse
    url(r'^browse/$', views.BrowseView.as_view()),        
    # User
    url(r'^@(?P<username>[^\.]+)$', views.UserprofileView.as_view(), name="user_profile"),        
    # Hub
    url(r'^hub/(?P<hubslug>[^\.]+)/$', views.HubView.as_view()),
    
    # CRUD Stories
    url(r'^post/create$', views.post_create),
    url(r'^post/(?P<slug>[^\.]+)/repost$', views.repost),
    url(r'^post/(?P<slug>[^\.]+)/edit$', views.post_edit),
    url(r'^post/(?P<slug>[^\.]+)/delete$', views.post_delete),

    # Replies
    url(r'^reply/(?P<parentslug>[^\.]+)', views.post_create),

    # View post
    url(r'^post/(?P<slug>[^\.]+)/?$', views.post, name='view_post'),

    url(r'^upvote/$', views.upvote),
    url(r'^unupvote/$', views.unupvote),

    
    # Other
    url(r'^hubs/$', views.HubList.as_view()),


    # Email
    url(r'^email/$', views.email),

    # Sandbox
    url(r'^sandbox/$', views.sandbox),


    
]



