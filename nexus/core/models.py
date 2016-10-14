from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink


class Settings(models.Model):
    title = models.CharField(max_length=64)    
    description = models.TextField(max_length=512, blank=True)
    about = models.TextField(default="", null=True, blank=True)
    guidelines = models.TextField(default="", null=True, blank=True)
    welcomepost = models.TextField(default="", null=True, blank=True) 

    
    def __str__(self):
        return self.title


        


