from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField()
    author = models.ForeignKey('auth.User')

    hubs =
    score = 
    
    pub_date = models.DateTimeField(default=timezone.now)


class Hub(models.Model):
    posts

    
class Comment(models.Model):
    author
    score

    date


class User(models.Model):                     # extend
    username =
    email =
    about =  
    karma =

    created =
    # First
    # Last


    
