from django.contrib import admin

from .models import  Story, Chapter

from hubs.models import Hub
from comments.models import Comment

class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Chapter, ChapterAdmin)

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Story, StoryAdmin)

class HubAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Hub, HubAdmin)    

admin.site.register(Comment)

