from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.posts_hot, name='hot_posts'), # hot
    url(r'^new/$', views.posts_new, name='new_posts'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),    
    url(r'^top/(?P<slug>[^\.]+)/$', views.posts_top, name='top_posts'),
    url(r'^hub/(?P<slug>[^\.]+)', views.hub_new, name='hub'),    

    url(r'^post/(?P<slug>[^\.]+)/edit', views.post_edit, name='post_edit'),        
    url(r'^post/(?P<slug>[^\.]+)', views.post, name='view_post'),
    # url(r'^user/(?P<username>[^\.]+)/top', views.user_top, name='user_top'),
    # url(r'^user/(?P<username>[^\.]+)/comments', views.user_comments, name='user_comments'),
    url(r'^user/(?P<username>[^\.]+)/about', views.about, name='about'),
    url(r'^user/(?P<username>[^\.]+)/subscribe', views.subscribe, name='subscribe'),
    url(r'^user/(?P<username>[^\.]+)/unsubscribe', views.unsubscribe, name='unsubscribe'),
    url(r'^preferences/$', views.user_prefs, name='preferences'),
    url(r'^user/(?P<username>[^\.]+)', views.user_new, name='user_new'),
    url(r'^about/$', views.about, name='about'),    
    url(r'^story/$', views.story, name='story'),
    url(r'^story-create/$', views.story_create),
    url(r'^story-edit/$', views.story_edit),    
    url(r'^chapter/$', views.chapter, name='chapter'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^prompt/$', views.prompt, name='prompt'),    

    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),        


    url('^login/$', views.login_or_signup, name='login'),
    # url(r'^login/', 'django.contrib.auth.views.login', {'template_name':'auth/login.html'}),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    url('^register/$', views.register, name='register'),
    url(r'^authenticate/', views.authenticate_user, name='authenticate'),
]
