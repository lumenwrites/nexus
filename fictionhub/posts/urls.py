from django.conf.urls import url

from . import views

urlpatterns = [
    # Post
    url(r'^post/(?P<story>[^\.]+)$', views.post, name='view_post'),

    # Challenges list
    url(r'^challenges/$', views.posts,
        {'filterby':'challenges'}),                

    # Submissions list
    url(r'^challenge/(?P<challenge>[^\.]+)/submissions$', views.posts,
        {'filterby':'challenge'}),                

    # Challenge
    url(r'^challenge/(?P<challenge>[^\.]+)/submit-story$', views.post_create),            
    url(r'^challenge/(?P<story>[^\.]+)$', views.post, name='view_challenge'),


    # url(r'^challenges/(?P<rankby>[^\.]+)/(?P<timespan>[^\.]+)/$', views.posts,
    #     {'filterby': 'challenges'}),    
    # url(r'^challenges/(?P<rankby>[^\.]+)/$', views.posts,
    #     {'filterby': 'challenges'}),    
    # url(r'^challenges/$', views.posts,
    #     {'filterby': 'challenges'}),    
    

    # import feed
    url(r'^user/(?P<username>[^\.]+)/feedimport$', views.feed_import),

    # Edit story
    url(r'^story/add$', views.post_create),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/edit$', views.post_edit),    
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/up$', views.chapter_up),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/down$', views.chapter_down),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/delete$', views.post_delete),        
    
    url(r'^story/(?P<story>[^\.]+)/edit$', views.post_edit),
    url(r'^story/(?P<story>[^\.]+)/delete$', views.post_delete),
    url(r'^story/(?P<story>[^\.]+)/publish$', views.post_publish),
    url(r'^story/(?P<story>[^\.]+)/unpublish$', views.post_unpublish),          
    url(r'^story/(?P<story>[^\.]+)/add$', views.post_create),


    
    # Rss
    url(r'^story/(?P<story>[^\.]+)/feed$', views.post_feed),        

    # JSON
    url(r'^story/(?P<slug>[^\.]+)/json$', views.post_json),        


    url(r'^404/', views.page_404),
    
    # Rank comments
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/comments/(?P<rankby>[^\.]+)$',
        views.post, name='view_story'),

    # Reviews
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/reviews$',
        views.post, 
        {'filterby': 'reviews'},
        name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/reviews$',
        views.post, 
        {'filterby': 'reviews'},
        name='view_story'),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/reviews/(?P<rankby>[^\.]+)$',
        views.post, 
        {'filterby': 'reviews'},
        name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)/reviews/(?P<rankby>[^\.]+)$',
        views.post, 
        {'filterby': 'reviews'},
        name='view_story'),


    # View story/chapter
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)$', views.post, name='view_chapter'), 
    url(r'^story/(?P<story>[^\.]+)$', views.post, name='view_story'),

    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),
    url(r'^unupvote/$', views.unupvote),
    url(r'^undownvote/$', views.undownvote),

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
