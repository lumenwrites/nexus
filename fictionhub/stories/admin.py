from django.contrib import admin

from .models import  Story, Chapter


class ChapterAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Chapter, ChapterAdmin)

class StoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Story, StoryAdmin)




