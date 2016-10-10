from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

class Hub(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")
    description = models.TextField(max_length=512, blank=True)
    
    def __str__(self):
        # try:
        #     parent_title = self.parent.title + " | "
        # except:
        #     parent_title = ""
        # return parent_title  + self.title
        return self.slug

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Hub, self).save(*args, **kwargs)
