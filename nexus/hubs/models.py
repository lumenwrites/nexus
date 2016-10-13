from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from core.utils import resize_image

class Hub(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")
    description = models.TextField(max_length=512, blank=True)

    background = models.ImageField(upload_to='hubs/backgrounds', default=None,blank=True, null=True)            

    moderators = models.ManyToManyField('profiles.User', related_name="hubs", blank=True, null=True, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        if self.background:
            resize_image(self.background, 480)        

        super(Hub, self).save(*args, **kwargs)

        
