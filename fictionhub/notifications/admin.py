from django.contrib import admin

from .models import  Message, Subject


class MessageAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',), }
    search_fields = ['body']

admin.site.register(Message, MessageAdmin)

class SubjectAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('title',), }
    search_fields = ['title']

admin.site.register(Subject, SubjectAdmin)
