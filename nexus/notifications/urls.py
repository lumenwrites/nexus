from django.conf.urls import url

from . import views
# from .views import HubCreate

urlpatterns = [
    # url(r'^notifications/(?P<notificationtype>[^\.]+)/$', views.notifications),
    url(r'^notifications/', views.notifications),    

    url(r'^send-emails/$', views.send_emails),            
    # url(r'^hub/add/$', views.hub_create),
    # url(r'^hub/add/$', HubCreate.as_view()),        
]
