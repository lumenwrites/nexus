from django.db import models

# Create your models here.
from django.conf import settings

# from hubs.models import Hub


class Message(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="out_messages", default="")
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="in_messages", default="") 
    subject = models.ForeignKey('Subject', related_name="messages",
                                default=None, null=True, blank=True)
    # title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, default="")
    body = models.TextField(default="", null=True, blank=True)

    pub_date = models.DateTimeField(auto_now_add=True)

    MESSAGE_TYPES = (
        ("message", "Message"),
        ("comment", "Comment"),
        ("review", "Review"),
        ("reply", "Reply"),
        ("subscriber", "Subscriber"),
        ("upvote", "Upvote"),
    )
    message_type = models.CharField(default="message", max_length=64, choices=MESSAGE_TYPES, blank=True)

    isread = models.BooleanField(default=False)                

class Subject(models.Model):    
    title = models.CharField(max_length=256)
