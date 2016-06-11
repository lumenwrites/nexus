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
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, default="")
    published = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(blank=True) # auto_now_add=True
    # (default=datetime.datetime.now, null=True, blank=True)
    # datetime.datetime.utcnow().replace(tzinfo=utc)
    # modified = models.DateTimeField()
    body = models.TextField(default="", null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", default="")

    hubs = models.ManyToManyField('hubs.Hub', related_name="posts", blank=True)
    score = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    wordcount = models.IntegerField(default=0)    

    imported = models.BooleanField(default=False)
    rational = models.BooleanField(default=False)
    daily = models.BooleanField(default=False)
    fictionhub = models.BooleanField(default=False)        

    parent = models.ForeignKey('Post', related_name="children",default=None, null=True, blank=True)

    POST_TYPES = (
        ("post", "Post"), # no children
        ("story", "Story"), # children are chapters
        ("chapter", "Chapter"), # no children
        ("thread", "Thread"), # no children
        ("prompt", "Prompt"), # children are other posts/stories        
        ("challenge", "Challenge"), # children are other posts/stories
        ("wiki", "Wiki"), # children are other posts/stories        
    )
    post_type = models.CharField(default="story", max_length=64, choices=POST_TYPES, blank=True)


    # Challenge
    CHALLENGE_STATES = (
    ("open", "Open"),
    ("voting", "Voting"),
    ("completed", "Completed"),    
    )
    state = models.CharField(default=None, max_length=64, choices=CHALLENGE_STATES, blank=True, null=True)    

    # Chapter
    number = models.IntegerField(default=1)        

    # reddit url
    reddit_url = models.URLField(max_length=256, blank=True, null=True, default="")

    approved = models.BooleanField(default=False)            

    def __str__(self):
        if self.post_type == "chapter" and self.parent:
            parent_title = self.parent.title + " | "
        else:
            parent_title = ""

        return parent_title + self.title

    def save(self, slug="", *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        # self.modified = datetime.datetime.today()

        if slug:
            # If I'm passing a slug - just use it.
            self.slug = slug            
        else:
            # If not - slugify title
            self.slug = orig = slugify(self.title)
            # Come up with unique id
            while True:
                # If the post is unique now - it's done, if not - come up with another one
                if not Post.objects.filter(slug=self.slug).exists():
                    break
                # Generate random id
                uniqueid = uuid.uuid1().hex[:5]
                self.slug = orig + "-" + str(uniqueid)
                
                

        try:
            if self.post_type == "chapter" and self.parent:
                self.author = self.parent.author
        except:
            pass


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
        if self.post_type == "post":
            return ('view_post', None, {'slug': self.slug })
        elif self.post_type == "story":
            return ('view_story', None, {'story': self.slug })
        elif self.post_type == "chapter":
            return ('view_chapter', None, {'chapter': self.slug,
                                            'story': self.parent.slug})            
        elif self.post_type == "challenge":
            return ('view_challenge', None, {'story': self.slug })            
        elif self.post_type == "prompt":
            return ('view_prompt', None, {'story': self.slug })
        elif self.post_type == "wiki":
            return ('view_wiki', None, {'story': self.slug })
        else:
            return ('view_post', None, {'story': self.slug })            

    class Meta:
        ordering = ('number',)
        unique_together = ["parent", "slug"]
        
