from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.hot_posts, name='hot_posts'), # hot
    url(r'^new/$', views.new_posts, name='new_posts'),
    url(r'^top/(?P<slug>[^\.]+)/$', views.top_posts, name='top_posts'),
    

    url(r'^post/(?P<slug>[^\.]+).html', views.post, name='view_post'),
    # url(r'^post/$', views.post, name='post'),            
    url(r'^user/$', views.user, name='user'),
    url(r'^about/$', views.about, name='about'),    
    url(r'^submit/$', views.submit, name='submit'),

    url(r'^upvote/$', views.upvote),
    url(r'^downvote/$', views.downvote),        

    url('^login/$', views.login_or_signup, name='login'),    
    url('^register/$', views.register, name='register'),
    url(r'^authenticate/', views.authenticate_user, name='authenticate'),
    

]
