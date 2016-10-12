from django.db import models

class Util(models.Model):
    ffnet_url = models.CharField(max_length=256)
    username_import = models.CharField(max_length=256, default="")
