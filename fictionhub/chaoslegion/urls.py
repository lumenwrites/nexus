from django.conf.urls import url

from . import views

urlpatterns = [
    #################### Posts ####################
    # Create/edit/delete
    url(r'^post/add$', views.submit, name='submit'),
    url(r'^prompt/$', views.prompt, name='prompt'), 
    url(r'^post/(?P<slug>[^\.]+)', views.post, name='view_post'),
    url(r'^post/(?P<slug>[^\.]+)/edit', views.post_edit, name='post_edit'),
    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),
    # TODO: delete post

    # List posts
    url(r'^$', views.posts_hot, name='hot_posts'),
    url(r'^new/$', views.posts_new, name='new_posts'),
    url(r'^top/(?P<slug>[^\.]+)/$', views.posts_top, name='top_posts'),
    url(r'^hub/(?P<slug>[^\.]+)', views.hub_new, name='hub'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),    
    # TODO: add sorting. View hot/top posts.
    
    

    #################### Stories ####################    
    url(r'^story/add$', views.story_create),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/edit$', views.chapter_edit),    
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/up$', views.chapter_up),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/down$', views.chapter_down),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)/delete$', views.chapter_delete),        
    
    url(r'^story/(?P<story>[^\.]+)/edit$', views.story_edit),
    url(r'^story/(?P<story>[^\.]+)/delete$', views.story_delete),      
    url(r'^story/(?P<story>[^\.]+)/add$', views.chapter_create),

    # View
    url(r'^user/(?P<username>[^\.]+)/stories', views.user_stories),
    url(r'^story/(?P<story>[^\.]+)/(?P<chapter>[^\.]+)$', views.chapter),            
    url(r'^story/(?P<story>[^\.]+)', views.story, name='view_story'),    
    
    url(r'^story/(?P<story>[^\.]+)/feed$', views.story_feed),    

    #################### User Page ####################
    url(r'^user/(?P<username>[^\.]+)/about', views.about, name='about'),
    url(r'^user/(?P<username>[^\.]+)/subscribe', views.subscribe, name='subscribe'),
    url(r'^user/(?P<username>[^\.]+)/unsubscribe', views.unsubscribe, name='unsubscribe'),
    url(r'^user/(?P<username>[^\.]+)', views.user_new, name='user_new'), # new posts
    url(r'^preferences/$', views.user_prefs, name='preferences'),
    # TODO: View top/hot posts, view user comments
    # url(r'^user/(?P<username>[^\.]+)/top', views.user_top, name='user_top'),
    # url(r'^user/(?P<username>[^\.]+)/comments', views.user_comments, name='user_comments'),
    
    #################### Auth ####################
    url('^login/$', views.login_or_signup, name='login'),
    # url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'auth/login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    url('^register/$', views.register, name='register'),
    url(r'^authenticate/', views.authenticate_user, name='authenticate'),
]
