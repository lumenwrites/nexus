from django.contrib import admin

from .models import User, Subscriber

admin.site.register(User)
admin.site.register(Subscriber)
