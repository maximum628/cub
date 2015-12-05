from django.contrib.auth.models import AbstractUser
from django.db import models
import mongoengine


class Account(AbstractUser):

    class Meta:
        app_label = 'app'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email', 'github_token')

    github_token = models.TextField(blank=False)
    name = models.CharField(max_length=128)
    github_url = models.URLField(blank=False)
    avatar_url = models.URLField()

    @classmethod
    def verify(cls, data):
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


class Contribution(mongoengine.Document):
    meta = {
        'abstract': True,
        'indexes': [{'fields': ['updated_at']}],
        'ordering': ['-updated_at']
    }

    cub_account = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True, unique_with='cub_account')
    url = mongoengine.URLField(required=True)
    html_repo_url = mongoengine.URLField(required=True)
    updated_at = mongoengine.DateTimeField(required=True)
    stats = mongoengine.DictField()


class CommitContribution(Contribution):

    files_stats = mongoengine.DictField()


class PRContribution(Contribution):

    title = mongoengine.StringField(required=True)
    state = mongoengine.StringField(required=True)

    @classmethod
    def create_or_update(cls, raw_data, account):
        if PRContribution.objects(
                cub_account=account.email, html_url=raw_data['html_url']):

            pr = PRContribution.objects.get(
                    cub_account=account.email, html_url=raw_data['html_url'])

            pr = pr.modify(
                url=raw_data['url'],
                html_repo_url=raw_data['html_url'].split('pull')[0],
                updated_at=raw_data['updated_at'],
                title=raw_data['title'],
                state=raw_data['state'])
        else:
            pr = PRContribution(
                cub_account=account.email,
                html_url=raw_data['html_url'],
                url=raw_data['url'],
                html_repo_url=raw_data['html_url'].split('pull')[0],
                updated_at=raw_data['updated_at'],
                title=raw_data['title'],
                state=raw_data['state']).save()
        return pr


class Repository(mongoengine.Document):

    meta = {
        'indexes': [{'fields': ['updated_at']}],
        'ordering': ['-updated_at']
    }

    cub_account = mongoengine.StringField(required=True)
    name = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True, unique_with='cub_account')
    url = mongoengine.URLField(required=True)
    created_at = mongoengine.DateTimeField(required=True)
    updated_at = mongoengine.DateTimeField(required=True)
    forks_count = mongoengine.IntField(required=True, default=0)
    stargazers_count = mongoengine.IntField(required=True, default=0)
    watchers_count = mongoengine.IntField(required=True, default=0)

    @classmethod
    def create_or_update(cls, raw_data, account):
        if Repository.objects(
                cub_account=account.email, html_url=raw_data['html_url']):

            repo = Repository.objects.get(
                    cub_account=account.email, html_url=raw_data['html_url'])

            repo = repo.modify(
                name=raw_data['name'],
                url=raw_data['url'],
                created_at=raw_data['created_at'],
                updated_at=raw_data['updated_at'],
                forks_count=raw_data['forks_count'],
                stargazers_count=raw_data['stargazers_count'],
                watchers_count=raw_data['watchers_count'])
        else:
            repo = Repository(
                cub_account=account.email,
                name=raw_data['name'],
                html_url=raw_data['html_url'],
                url=raw_data['url'],
                created_at=raw_data['created_at'],
                updated_at=raw_data['updated_at'],
                forks_count=raw_data['forks_count'],
                stargazers_count=raw_data['stargazers_count'],
                watchers_count=raw_data['watchers_count']).save()
        return repo


class Score(mongoengine.Document):

    cub_account = mongoengine.StringField(required=True, unique=True)
    score = mongoengine.IntField(required=True)

    @classmethod
    def compute(cls, email):
        watchers, stargazers_count, forks = Score.get_repo_stats(email)
        live_score =  watchers + stargazers_count + forks

        if Score.objects(cub_account=email):
            score = Score.objects.get(cub_account=email).modify(score=live_score)
        else:
            score = Score(cub_account=email, score=live_score).save()
        return score

    @classmethod
    def get_repo_stats(cls, email):
        watchers = 0
        stargazers = 0
        forks = 0

        for repo in Repository.objects(cub_account=email):
            watchers += repo.watchers_count
            stargazers += repo.stargazers_count
            forks += repo.forks_count

        return watchers, stargazers, forks
