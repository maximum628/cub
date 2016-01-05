from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie_mongoengine import resources

from app.models import (Account, CommitContribution, PRContribution, Repository,
    Score, Contact)

from app.authorization import (AccountOnlyAuthorization, ContactAuthorization,
    MyAccountOnlyAuthorization, AccountObjectsOnlyAuthorization)


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'github_token', 'password', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser']
        filtering = {'username': ALL, 'email': ALL, 'name': ALL}
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = AccountOnlyAuthorization()


class MyAccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'password', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'update']
        authentication = SessionAuthentication()
        authorization = MyAccountOnlyAuthorization()


class CommitContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = CommitContribution.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator


class PRContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = PRContribution.objects.all()
        resource_name = 'pulls'
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator


class RepositoryResource(resources.MongoEngineResource):
    class Meta:
        queryset = Repository.objects.all()
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator


class ScoreResource(resources.MongoEngineResource):
    class Meta:
        queryset = Score.objects.all()
        allowed_methods = ['get']
        excludes = ['live_score']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator


class ContactResource(resources.MongoEngineResource):
    class Meta:
        queryset = Contact.objects.all()
        allowed_methods = ['post']
        authorization = ContactAuthorization()
