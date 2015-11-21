from django.contrib.auth.hashers import make_password, check_password
from django.db import models

class Account(models.Model):

    class Meta:
        app_label = 'app'
        unique_together = (('username', 'email'),)

    username = models.CharField(max_length=50, unique=True, blank=False, null=False)
    github_token = models.TextField(blank=False, null=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, blank=False, null=False)
    github_url = models.URLField(blank=False, null=False)
    avatar_url = models.TextField()

    @classmethod
    def save(cls, data):
        if Account.objects.filter(username=data['username'], email=data['email']):
            account = Account.objects.get(username=data['username'], email=data['email'])

            if not check_password(data['github_token'], account.github_token):
                account.github_token = make_password(data['github_token'])
                account.save()
            return account
        else:
            return cls.create(data)

    @classmethod
    def create(cls, data):
        account = Account(
            username=data['username'], name=data['name'],
            email=data['email'], github_url=data['github_url'],
            avatar_url=data['avatar_url'])

        account.github_token = make_password(data['github_token'])
        account.save()
        return account

    @classmethod
    def authorize(cls, username, password):
        if Account.objects.filter(username=username):
            account = Account.objects.get(username=username)
            if check_password(password, account.github_token):
                return account
        return None
