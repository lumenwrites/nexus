from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import permalink

from posts.models import Post
from comments.models import Comment
from hubs.models import Hub

from core.utils import resize_image

class User(AbstractUser):  
    about = models.TextField(max_length=512, blank=True)
    website = models.CharField(max_length=64, blank=True)
    karma = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)


    avatar = models.ImageField(upload_to='profiles/avatars', default=None,blank=True, null=True)
    background = models.ImageField(upload_to='profiles/backgrounds', default=None,blank=True, null=True)        
    subscribed_to = models.ManyToManyField('User', related_name="subscribers", blank=True)
    subscribed_to_hubs = models.ManyToManyField('hubs.Hub', related_name="subscribers", blank=True)

    upvoted = models.ManyToManyField('posts.Post', related_name="upvoters", blank=True)
    reposted = models.ManyToManyField('posts.Post', related_name="reposters", blank=True) 
    
    # shadowban = models.BooleanField(default=False)
    # approved = models.BooleanField(default=False)

    new_notifications = models.BooleanField(default=False)    

    # Email notifications
    # email_subscriptions = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone I follow publishes a new story')
    # email_comments = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone replies to my story or comment')
    # email_messages = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone sends me a personal message.')
    # email_subscriber_notifications = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone subscribes to my stories.')
    # email_upvotes = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone upvotes my story.')
    # email_messages = models.BooleanField(default=True,
    # verbose_name='Send me email notifications when someone sends me a personal message.')
    
    # email_messages = models.BooleanField(default=False)                            


    def save(self, *args, **kwargs):
        if self.avatar:
            resize_image(self.avatar, 160)

        if self.background:
            resize_image(self.background, 480)        
        super(User, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return ('user_profile', None, {'username': self.username })        


# Email subscriber
class Subscriber(models.Model):
    email = models.CharField(max_length=64, blank=True)
    ref = models.CharField(max_length=64, blank=True, default="", null=True)        
    # subscribed_to = models.ManyToManyField('User', related_name="email_subscribers", blank=True, default=None)

    def __str__(self):
        if not self.ref:
            return self.email
        else:
            return self.ref + " | " + self.email
