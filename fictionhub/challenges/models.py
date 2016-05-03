import datetime

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

class Prompt(models.Model):
    prompt = models.TextField(default="", null=True, blank=True)
    slug = models.SlugField(max_length=64, default="")

    # reddit_url = models.URLField(max_length=256, blank=True, null=True, default="")
    # fetch_time =  models.DateTimeField(blank=True)

    # score = models.IntegerField(default=0)
    # position = models.IntegerField(default=0)
    # num_comments = models.IntegerField(default=0)
    # age = models.IntegerField(default=0)
    
    
    PROMPT_TYPES = (
        # ("prompt", "Prompt"),
        ("concept", "Concept"),        
        ("setting", "Setting"),
        ("character", "Character"),        
        ("problem", "Problem/Goal"),
        # ("wpsub", "wpsub"),
    )
    prompt_type = models.CharField(default="concept", max_length=64, choices=PROMPT_TYPES, blank=True)

    
    def __str__(self):
        return self.prompt

    def save(self, *args, **kwargs):
        self.slug = slugify(self.prompt[:32])
        if not self.id:
            self.fetch_time = datetime.datetime.now()

        return super(Prompt, self).save(*args, **kwargs)
