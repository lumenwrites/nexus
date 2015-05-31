from django.contrib import admin

from .models import Post, Hub, Comment, User, Story, Chapter

class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Chapter, ChapterAdmin)

admin.site.register(Post)
admin.site.register(Hub)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Story)
