from django.contrib import admin

from .models import Prompt

class PromptAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('prompt',), }

admin.site.register(Prompt, PromptAdmin)    

