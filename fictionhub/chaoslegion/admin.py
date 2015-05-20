from django.contrib import admin

from .models import Post, Hub, Comment, User

admin.site.register(Post)
admin.site.register(Hub)
admin.site.register(Comment)
admin.site.register(User)

