from django.conf.urls import url
from django.views.generic import RedirectView


from . import views, feeds, repost, editorial
# from .feeds import MainFeed

urlpatterns = [

    # User Feed
    url(r'^user/(?P<username>[^\.]+)/feed/atom/$', feeds.UserFeed()),    

    # Store
    url(r'^user/rayalez/store/$', views.item),
    url(r'^book/$', views.book),

    # Temp
    url(r'^wiki/rational-fiction$', RedirectView.as_view(url='/story/rational-fiction')),



    # Class Based Views
    # Browse
    url(r'^browse/$', views.BrowseView.as_view()),        
    # Subscriptions
    url(r'^subscriptions/$', views.SubscriptionsView.as_view()),    
    # User
    url(r'^user/(?P<username>[^\.]+)/$', views.UserprofileView.as_view()),
    url(r'^u/(?P<username>[^\.]+)/$', views.UserprofileView.as_view()),
    url(r'^@(?P<username>[^\.]+)$', views.UserprofileView.as_view(), name="user_profile"),        
    # Hub
    url(r'^hub/(?P<hubslug>[^\.]+)/$', views.HubView.as_view()),
    

    
    
    # Rank comments
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_story'),


    
    
    # CRUD Stories
    url(r'^write/$', views.post_create_daily),
    url(r'^story/add$', views.post_create),
    url(r'^post/create$', views.post_create),    
    url(r'^story/(?P<story>[^\.]+)/edit$', views.post_edit),
    url(r'^story/(?P<story>[^\.]+)/delete$', views.post_delete),
    url(r'^story/(?P<story>[^\.]+)/publish$', views.post_publish),
    url(r'^story/(?P<story>[^\.]+)/unpublish$', views.post_unpublish),          


    # View story/chapter
    url(r'^post/(?P<slug>[^\.]+)/?$', views.post, name='view_post'),

    url(r'^upvote/$', views.upvote),
    url(r'^unupvote/$', views.unupvote),

    
    # Other
    url(r'^hubs/$', views.HubList.as_view()),
    url(r'^series/$', views.SeriesList.as_view()),    


    # Email
    url(r'^email/$', views.email),

    # Sandbox
    url(r'^sandbox/$', views.sandbox),

    # Prompts
    url(r'^writing-prompts/$', views.writing_prompts),
    # Editorial
    url(r'^prompt/$', editorial.prompt),
    url(r'^promptsrepost/$', editorial.prompts_repost),

    # Browse old
    # url(r'^browse/$', views.browse),
    # url(r'^browse/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.browse),    
    # url(r'^browse/(?P<rankby>[^\.]+)/$', views.browse),    
    
]



# TODO: replace with Views.
# from django.conf.urls import url

# from .views import PostsView,  PostView, PostEdit, PostCreate

# urlpatterns = [

#     url(r'^story/create/?$',
#         PostCreate.as_view()),        

    
#     # Edit
#     url(r'^post/(?P<slug>[^\.]+)/edit/?$',
#         views.PostView.as_view(),
#         name="edit_post"),        
#     url(r'^story/(?P<slug>[^\.]+)/edit/?$',
#         PostEdit.as_view()),        

    
#     # View
#     url(r'^story/(?P<slug>[^\.]+)/?$',
#         PostView.as_view(),
#         name="view_post"),        

#     url(r'^story/(?P<story>[^\.]+)/?$',
#         PostView.as_view(),
#         {'posttype': "story",
#          'filterby': "hot"},
#         name="view_story"),        

#     url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/?$',
#         PostView.as_view(),
#         name="view_chapter"),        

#     # List
#     url(r'^stories/$', PostsView.as_view()),

#     # Rank
#     # url(r'^(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$',
#     #     PostView.as_view()),    
#     url(r'^stories/(?P<rankby>[^\.]+)/$',
#         PostsView.as_view()),    
    
# ]
