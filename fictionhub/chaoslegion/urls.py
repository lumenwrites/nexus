from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts/$', views.posts, name='posts'),
    url(r'^post/(?P<slug>[^\.]+).html', views.post, name='view_post'),
    # url(r'^post/$', views.post, name='post'),            
    url(r'^user/$', views.user, name='user'),
    url(r'^submit/$', views.submit, name='submit'),    

]
