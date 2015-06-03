from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from hubs.models import Hub
from comments.models import Comment

class Story(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    published = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stories", default="")

    hubs = models.ManyToManyField('hubs.Hub', related_name="stories", blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Story, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('view_story', None, { 'story': self.slug })        

class Chapter(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    number = models.IntegerField(default=1)        
    story = models.ForeignKey('Story', related_name="chapters", default="")    
    published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)    
    body = models.TextField()

    # Author's notes
    # Reviews
    # Comments

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Chapter, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, { 'slug': self.slug })

    class Meta:
        ordering = ('number',)        

        
