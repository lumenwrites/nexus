from django.db import models

# Create your models here.
from django.conf import settings

# from hubs.models import Hub


class Notification(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="out_notifications", default="")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="in_notifications", default="") 
    post = models.ForeignKey('posts.Post', default=None, null=True, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)

    NOTIFICATION_TYPES = (
        ("subscribe", "Subscriber"),
        ("reply", "Reply"),
        ("repost", "Reply"),        
        ("upvote", "Upvote"),
    )
    notification_type = models.CharField(default=None, max_length=64, choices=NOTIFICATION_TYPES, blank=True)

    isread = models.BooleanField(default=False)

    email_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.message_type + " from " + str(self.from_user) + " to " + str(self.to_user)
    

# class Subject(models.Model):    
#     title = models.CharField(max_length=256)
#     slug = models.SlugField(max_length=256, default="")
