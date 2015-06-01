from django.db import models
from django.contrib.auth.models import AbstractUser

from stories.models import Story

class User(AbstractUser):  
    about = models.TextField(max_length=512, blank=True)
    external_url = models.BooleanField(default=False)
    website = models.CharField(max_length=32, blank=True)
    karma = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    subscribed_to = models.ManyToManyField('User', related_name="subscribers", blank=True)

    upvoted = models.ManyToManyField('stories.Story', related_name="upvoters", blank=True)
    downvoted = models.ManyToManyField('stories.Story', related_name="downvoters", blank=True)    

    comments_upvoted = models.ManyToManyField('stories.Comment', related_name="upvoters", blank=True)
    comments_downvoted = models.ManyToManyField('stories.Comment', related_name="downvoters", blank=True)    
    
