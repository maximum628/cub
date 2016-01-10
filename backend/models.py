import os
import datetime

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
import mongoengine

from cub.settings import CONTACT_ADMINS, EMAIL_HOST_USER, BASE_DIR


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


class AbstractJSONDocument(mongoengine.Document):

    meta = {'abstract': True}

    @classmethod
    def save_document(cls, data):
        document = cls()
        for key, value in data.iteritems():
            setattr(document, key, value)
        document.save()
        return document


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
                cub_account=account, html_url=raw_data['html_url']):

            pr = PRContribution.objects.get(
                    cub_account=account, html_url=raw_data['html_url'])

            pr = pr.modify(
                url=raw_data['url'],
                html_repo_url=raw_data['html_url'].split('pull')[0],
                updated_at=raw_data['updated_at'],
                title=raw_data['title'],
                state=raw_data['state'])
        else:
            pr = PRContribution(
                cub_account=account,
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
    description = mongoengine.StringField(required=True)
    html_url = mongoengine.URLField(required=True, unique_with='cub_account')
    url = mongoengine.URLField(required=True)
    created_at = mongoengine.DateTimeField(required=True)
    updated_at = mongoengine.DateTimeField(required=True)
    fork = mongoengine.StringField(required=True)
    forks_count = mongoengine.IntField(required=True, default=0)
    stargazers_count = mongoengine.IntField(required=True, default=0)
    watchers_count = mongoengine.IntField(required=True, default=0)
    open_issues = mongoengine.IntField(required=True, default=0)
    closed_issues = mongoengine.IntField(required=True, default=0)
    affiliation = mongoengine.StringField(required=True, default='unknown')

    @classmethod
    def create_or_update(cls, raw_data, account):
        if Repository.objects(
                cub_account=account, html_url=raw_data['html_url']):

            repo = Repository.objects.get(
                    cub_account=account, html_url=raw_data['html_url'])

            repo = repo.modify(
                name=raw_data['name'],
                description=raw_data['description'],
                url=raw_data['url'],
                created_at=raw_data['created_at'],
                updated_at=raw_data['updated_at'],
                forks_count=raw_data['forks'],
                fork=str(raw_data['fork']),
                stargazers_count=raw_data['stargazers_count'],
                watchers_count=raw_data['watchers_count'],
                open_issues=raw_data['open_issues_count'],
                affiliation=raw_data['affiliation'])
        else:
            repo = Repository(
                cub_account=account,
                name=raw_data['name'],
                description=raw_data['description'],
                html_url=raw_data['html_url'],
                url=raw_data['url'],
                created_at=raw_data['created_at'],
                updated_at=raw_data['updated_at'],
                forks_count=raw_data['forks'],
                fork=str(raw_data['fork']),
                stargazers_count=raw_data['stargazers_count'],
                watchers_count=raw_data['watchers_count'],
                open_issues=raw_data['open_issues_count'],
                affiliation=raw_data['affiliation']).save()
        return repo


class Score(mongoengine.Document):

    cub_account = mongoengine.StringField(required=True, unique=True)
    score = mongoengine.IntField(required=True)
    watchers_count = mongoengine.IntField()
    forks_count = mongoengine.IntField()
    stargazers_count = mongoengine.IntField()

    @classmethod
    def compute(cls, account):
        watchers, stargazers, forks = Score.get_repo_stats(account)
        live_score =  watchers + stargazers + forks

        if Score.objects(cub_account=account):
            score = Score.objects.get(cub_account=account).modify(
                score=live_score, watchers_count=watchers,
                forks_count=forks, stargazers_count=stargazers)
        else:
            score = Score(cub_account=account, score=live_score,
                watchers_count=watchers, forks_count=forks,
                stargazers_count=stargazers).save()
        return score

    @classmethod
    def get_repo_stats(cls, account):
        watchers = 0
        stargazers = 0
        forks = 0

        for repo in Repository.objects(cub_account=account):
            watchers += repo.watchers_count
            stargazers += repo.stargazers_count
            forks += repo.forks_count

        return watchers, stargazers, forks


class Contact(AbstractJSONDocument):

    meta = {
        'indexes': [{'fields': ['email']}]
    }

    name = mongoengine.StringField(required=True)
    email = mongoengine.EmailField(required=True)
    content = mongoengine.StringField(required=True)
    created_at = mongoengine.DateTimeField(required=True, default=datetime.datetime.now)

    @classmethod
    def send_email(cls, sender, document, **kwargs):
        msg_html = render_to_string(
            '%s/backend/templates/email/contact/notify_team.html' % BASE_DIR,
            {'document': document})

        send_mail(
            subject='CUB - Feedback received',
            message='New Feedback was received.',
            html_message=msg_html,
            from_email='Connect Hub - CUB <%s>' % EMAIL_HOST_USER,
            recipient_list=CONTACT_ADMINS,
            fail_silently=True)


        msg_html = render_to_string(
            '%s/backend/templates/email/contact/confirm_user.html' % BASE_DIR,
            {'document': document})

        send_mail(
            subject='CUB - Feedback sent',
            message='We confirm we received your feedback message.',
            html_message=msg_html,
            from_email='Connect Hub - CUB <%s>' % EMAIL_HOST_USER,
            recipient_list=CONTACT_ADMINS,
            fail_silently=True)

mongoengine.signals.post_save.connect(Contact.send_email, sender=Contact)
