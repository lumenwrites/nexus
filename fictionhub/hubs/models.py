from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

class Hub(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")
    description = models.TextField(default="", blank=True)
    parent = models.ForeignKey('Hub', related_name="children", default=None,null=True, blank=True)
    users_can_create_children = models.BooleanField(default=False)    
    description = models.TextField(max_length=512, blank=True)

    HUB_TYPES = (
        ("hub", "Hub"),
        ("folder", "Folder"),
    )
    hub_type = models.CharField(default="hub", max_length=64, choices=HUB_TYPES, blank=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        # try:
        #     parent_title = self.parent.title + " | "
        # except:
        #     parent_title = ""
        # return parent_title  + self.title
        return self.title        

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Hub, self).save(*args, **kwargs)
