from django.contrib import admin

from .models import  Notification


# class MessageAdmin(admin.ModelAdmin):
#     # prepopulated_fields = {'slug': ('title',), }
#     search_fields = ['body']

admin.site.register(Notification)

# class SubjectAdmin(admin.ModelAdmin):
#     # prepopulated_fields = {'slug': ('title',), }
#     search_fields = ['title']

# admin.site.register(Subject, SubjectAdmin)
