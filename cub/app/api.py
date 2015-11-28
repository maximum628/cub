from tastypie.resources import ModelResource
from tastypie_mongoengine import resources

from app.models import (Account, CommitContribution, PRContribution, Repository,
    Score)


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['github_token', 'id']
        allowed_methods = ['get']


class CommitContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = CommitContribution.objects.all()
        allowed_methods = ['get']


class PRContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = PRContribution.objects.all()
        allowed_methods = ['get']


class RepositoryResource(resources.MongoEngineResource):
    class Meta:
        queryset = Repository.objects.all()
        allowed_methods = ['get']
