from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hot_posts, name='hot_posts'), # hot
    url(r'^new/$', views.new_posts, name='new_posts'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),    
    url(r'^top/(?P<slug>[^\.]+)/$', views.top_posts, name='top_posts'),
    url(r'^hub/(?P<slug>[^\.]+)', views.hub_new, name='hub'),    

    url(r'^post/(?P<slug>[^\.]+)', views.post, name='view_post'),
    # url(r'^user/(?P<username>[^\.]+)/top', views.user_top, name='user_top'),
    # url(r'^user/(?P<username>[^\.]+)/comments', views.user_comments, name='user_comments'),
    url(r'^user/(?P<username>[^\.]+)/about', views.about, name='about'),
    url(r'^user/(?P<username>[^\.]+)/subscribe', views.subscribe, name='subscribe'),
    url(r'^user/(?P<username>[^\.]+)/unsubscribe', views.unsubscribe, name='unsubscribe'),
    url(r'^user/(?P<username>[^\.]+)', views.user_new, name='user_new'),
    url(r'^about/$', views.about, name='about'),    
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
