from django.contrib import admin

from .models import Hub

class HubAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Hub, HubAdmin)    

