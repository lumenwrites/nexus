from django.db import models

# class Quest(models.Model): - Story
#     title = models.CharField(max_length=256)
#     slug = models.SlugField(max_length=256, default="")
#     published = models.BooleanField(default=False, blank=True)
#     pub_date = models.DateTimeField(auto_now_add=True)

#     description = models.TextField(default="", null=True, blank=True)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", default="")
    
# class Move(models.Model): - Chapter
#     # number? id?    
#     # title = models.CharField(max_length=256)
#     # slug = models.SlugField(max_length=256, default="")
#     published = models.BooleanField(default=False, blank=True)
#     pub_date = models.DateTimeField(auto_now_add=True)

#     body = models.TextField(default="", null=True, blank=True)
#     author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="posts", default="")
    

class Votebox(models.Model):
    title = models.CharField(max_length=256)
    # options = foreign key
    # timer?
    

# class Option(models.Model): - Comment
#     description = models.TextField(default="", null=True, blank=True)
#     score = models.IntegerField(default=0)
