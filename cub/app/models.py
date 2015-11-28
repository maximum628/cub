from django.contrib.auth.hashers import make_password, check_password
from django.db import models
import mongoengine


class Account(models.Model):

    class Meta:
        app_label = 'app'

    username = models.CharField(max_length=128, blank=False)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, blank=False)
    github_token = models.TextField(blank=False)
    github_url = models.URLField(blank=False)
    avatar_url = models.URLField()

    @classmethod
    def verify(cls, data):
        if Account.objects.filter(username=data['username'], email=data['email']):
            account = Account.objects.get(
                username=data['username'], email=data['email'])

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
            avatar_url=data['avatar_url'], github_token=data['github_token'])

        account.github_token = make_password(data['github_token'])
        account.save()
        return account


class Contribution(mongoengine.Document):
    meta = {
        'abstract': True,
        'indexes': [{'fields': ['created_date']}],
        'ordering': ['-created_date']
    }

    account = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True)
    url = mongoengine.URLField(required=True)
    html_repo_url = mongoengine.URLField(required=True)
    repo_url = mongoengine.URLField(required=True)
    created_date = mongoengine.DateTimeField(required=True)
    stats = mongoengine.DictField()


class CommitContribution(Contribution):

    files_stats = mongoengine.DictField()


class PRContribution(Contribution):

    PR_STATES = (('Open', 'open'), ('Closed', 'closed'), ('All', 'all'))

    state = mongoengine.StringField(required=True, choices=PR_STATES)


class Repository(mongoengine.Document):

    account = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True)
    url = mongoengine.URLField(required=True)
    created_at = mongoengine.DateTimeField(required=True)
    updated_at = mongoengine.DateTimeField(required=True)
    forks_count = mongoengine.IntField(required=True, default=0)
    stargazers_count = mongoengine.IntField(required=True, default=0)
    watchers_count = mongoengine.IntField(required=True, default=0)


class Score(mongoengine.Document):

    account = mongoengine.StringField(required=True)
    score = mongoengine.IntField(required=True)
