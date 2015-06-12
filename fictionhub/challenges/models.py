from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink


class Challenge(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    published = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="challenges", default="")

    score = models.IntegerField(default=0)

    imported = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super(Story, self).save(*args, **kwargs)

    def save(self, slug="", *args, **kwargs):
        if self.imported == True and slug != "":
            self.slug = slug            
        else:
            self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return ('view_story', None, { 'story': self.slug })        
