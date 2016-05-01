from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import permalink

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

    rational = models.BooleanField(default=False)
    daily = models.BooleanField(default=False)    

    target_wordcount = models.IntegerField(default=250)
    
    shadowban = models.BooleanField(default=False)

    approved = models.BooleanField(default=False)

    new_notifications = models.BooleanField(default=False)    

    # Email notifications
    email_subscriptions = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone I follow publishes a new story')
    email_comments = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone replies to my story or comment')
    email_messages = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone sends me a personal message.')
    email_subscribers = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone subscribes to my stories.')
    email_upvotes = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone upvotes my story.')
    email_messages = models.BooleanField(default=True,
    verbose_name='Send me email notifications when someone sends me a personal message.')
    
    
    
    # email_messages = models.BooleanField(default=False)                            

    enable_dark_interface = models.BooleanField(default=False)    
    
    # @permalink
    # def get_absolute_url(self):
    #     return ('view_post', None, {'slug': self.slug })        
