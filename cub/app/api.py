from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.resources import ModelResource
from tastypie_mongoengine import resources

from app.models import (Account, CommitContribution, PRContribution, Repository,
    Score)


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'github_token', 'password', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()


class CommitContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = CommitContribution.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()


class PRContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = PRContribution.objects.all()
        resource_name = 'pulls'
        allowed_methods = ['get']
        authentication = SessionAuthentication()


class RepositoryResource(resources.MongoEngineResource):
    class Meta:
        queryset = Repository.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
