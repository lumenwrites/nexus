from django.db import models
from django.contrib.auth.models import AbstractUser

from posts.models import Post
from comments.models import Comment
from hubs.models import Hub

class User(AbstractUser):  
    about = models.TextField(max_length=512, blank=True)
    external_url = models.BooleanField(default=False)
    website = models.CharField(max_length=64, blank=True)
    rss_feed = models.CharField(max_length=128, blank=True, null=True, default="")
    categories_to_import = models.CharField(max_length=128, blank=True, null=True, default="")
    karma = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    subscribed_to = models.ManyToManyField('User', related_name="subscribers", blank=True)
    subscribed_to_hubs = models.ManyToManyField('hubs.Hub', related_name="subscribers", blank=True)

    upvoted = models.ManyToManyField('posts.Post', related_name="upvoters", blank=True)
    downvoted = models.ManyToManyField('posts.Post', related_name="downvoters", blank=True)   

    comments_upvoted = models.ManyToManyField('comments.Comment', related_name="upvoters", blank=True)
    comments_downvoted = models.ManyToManyField('comments.Comment', related_name="downvoters", blank=True)    

    rational = models.BooleanField(default=True)

    shadowban = models.BooleanField(default=False)

    approved = models.BooleanField(default=False)            
