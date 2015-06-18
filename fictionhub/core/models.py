from django.db import models

class Util(models.Model):
    ffnet_url = models.CharField(max_length=256)
