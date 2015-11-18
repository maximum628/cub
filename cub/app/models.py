from django.db import models

class Account(models.Model):

    class Meta:
        app_label = 'app'

    github_url = models.URLField()
    github_token = models.TextField()
    avatar_url = models.TextField()
