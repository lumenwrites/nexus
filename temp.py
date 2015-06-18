# coding: utf-8

from posts.models import Post
posts = Post.objects.all()
for post in posts:
    post.rational = True
    post.save()
    
get_ipython().magic('copy')
get_ipython().magic('save temp 0-5')
