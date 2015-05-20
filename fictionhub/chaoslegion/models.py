from django.db import models

from django.conf import settings

# Import User if you want to link UserProfile to it:
# from django.contrib.auth.models import User
# But I'm replacing it instead:
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)

    hubs = models.ForeignKey('Hub')
    score = models.IntegerField(default=0)
    
    pub_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title    


class Hub(models.Model):
    pass
    # posts ? already created in posts?

    
class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    
class User(AbstractUser):  
    about = models.TextField(max_length=512, blank=True)
    karma = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

#link        
# class User(models.Model):
#    user = models.OneToOneField(User)
##     username = models.CharField(max_length=32)
#     email = models.EmailField()
#     about = models.TextField()
    
#     karma = models.IntegerField(default=0)

#     created = models.DateTimeField(default=timezone.now)
#     # First models.CharField(max_length=30)
#     # Last




