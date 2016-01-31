from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):

    class Meta:
        app_label = 'backend'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'github_token')

    github_token = models.TextField(blank=False)
    name = models.CharField(max_length=128)
    github_url = models.URLField(blank=False)
    avatar_url = models.URLField()
    synced = models.IntegerField(null=True)

    @classmethod
    def verify(cls, data):
        """ Ensure the github token and password are updated when the OAuth2
        communication returns a new token from GitHub.
        """
        if Account.objects.filter(username=data['username'], email=data['email']):
            account = Account.objects.get(
                username=data['username'], email=data['email'])

            if data['github_token'] != account.github_token:
                account.set_password(data['github_token'])
                account.github_token = data['github_token']
                account.save()
            return account
        else:
            return cls.create(data)

    @classmethod
    def create(cls, data):
        account = Account(
            username=data['username'], name=data['name'],
            email=data['email'], github_url=data['github_url'],
            avatar_url=data['avatar_url'], github_token=data['github_token'])

        account.set_password(data['github_token'])
        account.save()
        return account
