"""fictionhub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# from chaoslegion import urls as chaoslegion_urls
from profiles import urls as profiles_urls
from hubs import urls as hubs_urls
from challenges import urls as challenges_urls
from posts import urls as posts_urls
from comments import urls as comments_urls
from notifications import urls as notifications_urls

from quests import urls as quests_urls


from . import views


from posts import views as posts_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include(profiles_urls)),
    url(r'', include(hubs_urls)),
    url(r'', include(challenges_urls)),    
    url(r'', include(comments_urls)),
    url(r'', include(posts_urls)),
    url(r'', include(notifications_urls)),        

    url(r'', include(quests_urls)),    

    url(r'^test/$', views.test),
    url(r'^about/$', views.about),
    url(r'^submit/$', views.submit),
    url(r'^store/$', views.store),        
    url(r'^join/$', views.home),                
    
    # Front page
    url(r'^$', views.home),
    url(r'^$', posts_views.BrowseView.as_view()),

    url(r'^404/', views.page_404),    

    # url(r'.*', stories.views.page_404),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
