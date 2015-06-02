from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink


class Story(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    published = models.BooleanField(default=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stories")

    hubs = models.ManyToManyField('Hub', related_name="stories", blank=True)
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
    story = models.ForeignKey('Story', related_name="chapters")    
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

class Hub(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")
    # description = models.TextField(dafault="", blank=True)
    parent = models.ForeignKey('Hub', related_name="children", default=None,null=True, blank=True)
    # users_can_create_children = models.BooleanField(default=True)    
    
    def __str__(self):
        return self.title    

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Hub, self).save(*args, **kwargs)
    

class Comment(models.Model):
    story = models.ForeignKey('Story', related_name="comments",
                              default=None, null=True, blank=True)
    chapter = models.ForeignKey('Chapter', related_name="comments",
                                default=None,  null=True, blank=True)    
    parent = models.ForeignKey('Comment', related_name="children",
                               default=None, null=True, blank=True)
    body = models.TextField()    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    COMMENT_TYPES = (
    (u'1', u'Comment'),
    (u'2', u'Review'),
    )    
    comment_type = models.CharField(max_length=64, default="Comment", choices=COMMENT_TYPES)

    def __str__(self):
        string_name = ""
        try:
            string_name = self.body # self.story.title + self.body
        except:
            string_name = self.body # self.chapter.title + self.body  
        return string_name
    
        
