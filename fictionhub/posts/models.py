import datetime
import itertools
import re
import uuid
from string import punctuation

from django.utils.timezone import utc

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from hubs.models import Hub
from comments.models import Comment

class Post(models.Model):
    title = models.SlugField(max_length=256, default="", blank=True)    
    slug = models.SlugField(max_length=256, default="")
    pub_date = models.DateTimeField(blank=True)
    body = models.TextField(default="", null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", default="")

    hubs = models.ManyToManyField('hubs.Hub', related_name="posts", blank=True)
    score = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    wordcount = models.IntegerField(default=0)    

    parent = models.ForeignKey('Post', related_name="children",default=None, null=True, blank=True)


    # approved = models.BooleanField(default=False)            

    def __str__(self):
        return self.body[:140]

    def save(self, slug="", *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        # self.modified = datetime.datetime.today()

        if self.pk is None:            
            if slug:
                # If I'm passing a slug - just use it.
                # As it stands - don't need it, I'm never editing it once created.
                self.slug = slug            
            else:
                # If not - slugify title
                uniqueid = uuid.uuid1().hex[:5]                
                self.slug = orig = uniqueid
                # Come up with unique id
                while True:
                    # If the post is unique now - it's done, if not - come up with another one
                    if not Post.objects.filter(slug=self.slug).exists():
                        break
                    # Generate random id
                    uniqueid = uuid.uuid1().hex[:5]
                    self.slug = str(uniqueid)
                    

        # Count words
        r = re.compile(r'[{}]'.format(punctuation))
        wordcount = 0
        text = r.sub(' ',self.body)
        wordcount += len(text.split())
        if self.children:
            for child in self.children.all():
                text = r.sub(' ',child.body)
                wordcount += len(text.split())
        self.wordcount = wordcount

            
        return super(Post, self).save(*args, **kwargs)
    
    @permalink
    def get_absolute_url(self):
        return ('view_post', None, {'slug': self.slug })

    # class Meta:
    #     ordering = ('number',)
    #     unique_together = ["parent", "slug"]
        
