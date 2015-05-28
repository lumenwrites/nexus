from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink
# Import User if you want to link UserProfile to it:
# from django.contrib.auth.models import User
# But I'm replacing it instead:
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    published = models.BooleanField(default=True) # change to false when I have save draft?
    body = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts")
    
    hubs = models.ManyToManyField('Hub', related_name="posts", blank=True)
    score = models.IntegerField(default=0)
    # story = models.ForeignKey('Story', related_name="chapters")
    
    
    pub_date = models.DateTimeField(auto_now_add=True)

    #//add bookmarks

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    # Response from get_absolute_url: /blog/view/how-to-create-a-basic-blog-in-django.html
    @permalink
    def get_absolute_url(self):
        return ('view_post', None, { 'slug': self.slug })        

class Story(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
    published = models.BooleanField(default=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="stories")

    hubs = models.ManyToManyField('Hub', related_name="stories", blank=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, { 'slug': self.slug })        

class Chapter(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length=256, unique=True, default="")
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
        super(Post, self).save(*args, **kwargs)

    @permalink
    def get_absolute_url(self):
        return ('view_post', None, { 'slug': self.slug })        
    

class Hub(models.Model):
    title = models.CharField(max_length=64)    
    slug = models.SlugField(max_length=64, default="")

    def __str__(self):
        return self.title    
    

    
class Comment(models.Model):
    post = models.ForeignKey('Post', related_name="comments", default=None)
    parent = models.ForeignKey('Comment', related_name="children", null=True, default=None)
    body = models.TextField()    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments")
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title
    
    
class User(AbstractUser):  
    about = models.TextField(max_length=512, blank=True)
    external_url = models.BooleanField(default=False)
    website = models.CharField(max_length=32, blank=True)
    karma = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    # Add subscriptions
    subscribed_to = models.ManyToManyField('User', related_name="subscribers", blank=True)

    # Voted
    upvoted = models.ManyToManyField('Post', related_name="upvoters", blank=True)
    downvoted = models.ManyToManyField('Post', related_name="downvoters", blank=True)    


#link        
# class User(models.Model):
#    user = models.OneToOneField(User)
##     username = models.CharField(max_length=32)
#     email = models.EmailField()
#     about = models.TextField()
    
#     karma = models.IntegerField(default=0)

#     created = models.DateTimeField(default=timezone.now)
#     # First models.CharField(max_length=30)
#     # Last




