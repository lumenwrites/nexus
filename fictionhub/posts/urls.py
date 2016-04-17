from django.conf.urls import url

from . import views
from .views import MainFeed

urlpatterns = [
    # Store
    url(r'^user/rayalez/store/$', views.item),
    
    # Post
    url(r'^post/add$', views.post_create,
        {'posttype':'post'}),

    #book
    url(r'^book/$', views.book),

    
    # Rank comments
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_story'),


    
    
    # Edit story
    url(r'^story/add$', views.post_create),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/edit$', views.post_edit),    
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/delete$', views.post_delete),        
    url(r'^story/(?P<story>[^\.]+)/edit$', views.post_edit),
    url(r'^story/(?P<story>[^\.]+)/delete$', views.post_delete),
    url(r'^story/(?P<story>[^\.]+)/publish$', views.post_publish),
    url(r'^story/(?P<story>[^\.]+)/unpublish$', views.post_unpublish),          
    url(r'^story/(?P<story>[^\.]+)/add$', views.post_create),


    
    # Rss
    url(r'^feed/$', MainFeed()),            
    url(r'^story/(?P<story>[^\.]+)/feed$', views.post_feed),        


    url(r'^404/', views.page_404),


    # View story/chapter
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/?$', views.post, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/?$', views.post, name='view_story'),

    url(r'^upvote/$', views.upvote),
    url(r'^unupvote/$', views.unupvote),

    # List stories
    # User
    # Subscriptions
    url(r'^user/(?P<username>[^\.]+)/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.posts,
        {'filterby': 'user'}),    
    url(r'^user/(?P<username>[^\.]+)/(?P<rankby>[^\.]+)/$', views.posts,
        {'filterby': 'user'}),    
    url(r'^user/(?P<username>[^\.]+)/$', views.posts,
        {'filterby': 'user'}),    

    # Shorthand
    url(r'^u/(?P<username>[^\.]+)$', views.posts,
        {'filterby': 'user'}),    
    
    
    # Subscriptions
    url(r'^subscriptions/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.posts,
        {'filterby': 'subscriptions'}),    
    url(r'^subscriptions/(?P<rankby>[^\.]+)/$', views.posts,
        {'filterby': 'subscriptions'}),    
    url(r'^subscriptions/$', views.posts,
        {'filterby': 'subscriptions'}),    


    url(r'^hubs/$', views.HubList.as_view()),
    url(r'^series/$', views.SeriesList.as_view()),    
    # By hub
    url(r'^hub/(?P<hubslug>[^\.]+)/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.posts,
        {'filterby': 'hub'}),    
    url(r'^hub/(?P<hubslug>[^\.]+)/(?P<rankby>[^\.]+)/$', views.posts,
        {'filterby': 'hub'}),    
    url(r'^hub/(?P<hubslug>[^\.]+)/$', views.posts,
        {'filterby': 'hub'}),


    # No filter, just rank.
    url(r'^stories/$', views.posts),
    url(r'^stories/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.posts),    
    url(r'^stories/(?P<rankby>[^\.]+)/$', views.posts),    
    # url(r'^story/(?P<story>[^\.]+)/feed$', views.post_feed),

    # url(r'^$', views.browse),
    url(r'^browse/$', views.browse),
    url(r'^browse/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.browse),    
    url(r'^browse/(?P<rankby>[^\.]+)/$', views.browse),    

    # Email
    url(r'^email/$', views.email),

    # Sandbox
    url(r'^sandbox/$', views.sandbox),

    # Prompts
    url(r'^writing-prompts/$', views.writing_prompts),
    # Editorial
    url(r'^prompt/$', views.prompt),
    url(r'^promptsrepost/$', views.prompts_repost),
]



# TODO: replace with CBVs.
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
