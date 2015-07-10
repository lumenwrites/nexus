from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models import permalink

from posts.models import *

class Comment(models.Model):
    post = models.ForeignKey('posts.Post', related_name="comments",
                              default=None, null=True, blank=True)
    parent = models.ForeignKey('Comment', related_name="children",
                               default=None, null=True, blank=True)
    body = models.TextField()    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="comments", default="")
    score = models.IntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True)

    # COMMENT_TYPES = (
    # (u'1', u'Comment'),
    # (u'2', u'Review'),
    # )    
    # comment_type = models.CharField(max_length=64, default="Comment", choices=COMMENT_TYPES)

    COMMENT_TYPES = (
    ("comment", "Comment"),
    ("review", "Review"),
    )
    comment_type = models.CharField(default="comment", max_length=64, choices=COMMENT_TYPES, blank=True)

    RATING_CHOICES = [
        (1, "Horrible"),
        (2, "Bad"),
        (3, "Okay"),
        (4, "Good"),
        (5, "Brilliant"),
    ]
    rating = models.IntegerField(default=None, null=True, blank=True, choices=RATING_CHOICES)    

    def __str__(self):
        string_name = ""
        try:
            string_name = self.body # self.story.title + self.body
        except:
            string_name = "comment" #self.body # self.chapter.title + self.body
        if len(string_name) > 64:
            string_name = string_name[:64] + "..."
        return string_name
    

    @permalink
    def get_absolute_url(self):
        return ('view_comment', None, { 'story': self.post.slug,
                                            'comment_id': self.id })
        
