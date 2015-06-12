from django.contrib import admin

from .models import  Challenge

class ChallengeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',), }

admin.site.register(Challenge, ChallengeAdmin)
