from tastypie import fields
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import Authorization, DjangoAuthorization
from tastypie.constants import ALL
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie_mongoengine import resources

from backend.contribution import get_repos, get_pulls, get_score, get_commits
from backend.models.account import Account
from backend.models.contribution import CommitContribution, PRContribution
from backend.models.repository import Repository
from backend.models.score import  Score

from backend.authorization import (MyAccountOnlyAuthorization,
    AccountObjectsOnlyAuthorization)


class BaseAccountResource(ModelResource):
    forks_count = fields.IntegerField()
    stargazers_count = fields.IntegerField()
    watchers_count = fields.IntegerField()
    pulls_count = fields.IntegerField()

    def dehydrate_forks_count(self, bundle):
        try:
            score = Score.objects.get(cub_account=bundle.obj.username).forks_count
        except:
            score = 0
        return score

    def dehydrate_stargazers_count(self, bundle):
        try:
            score = Score.objects.get(cub_account=bundle.obj.username).stargazers_count
        except:
            score = 0
        return score

    def dehydrate_watchers_count(self, bundle):
        try:
            score = Score.objects.get(cub_account=bundle.obj.username).watchers_count
        except:
            score = 0
        return score

    def dehydrate_pulls_count(self, bundle):
        try:
            score = PRContribution.objects.filter(cub_account=bundle.obj.username).count()
        except:
            score = 0
        return score


class AccountResource(BaseAccountResource):
    """ All accounts resources, available if a user is signed in, lists all
        details for an account.
    """

    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'github_token', 'password', 'is_active', 'is_staff',
                    'is_superuser', 'first_name', 'last_name', 'synced', 'last_login']
        filtering = {'username': ALL, 'name': ALL}
        allowed_methods = ['get']
        authentication = SessionAuthentication()


class MyAccountResource(BaseAccountResource):

    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'password', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        authentication = SessionAuthentication()
        authorization = MyAccountOnlyAuthorization()


class CommitContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = CommitContribution.objects.all()
        resource_name = 'commits'
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator

    def obj_create(self, bundle, request = None, **kwargs):
        get_commits(bundle.obj.username)
        bundle.obj.data = {}
        return bundle


class PRContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = PRContribution.objects.all()
        resource_name = 'pulls'
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator

    def obj_create(self, bundle, request = None, **kwargs):
        get_pulls(bundle.obj.github_token, bundle.obj.username)
        bundle.obj.data = {}
        return bundle


class RepositoryResource(resources.MongoEngineResource):
    class Meta:
        queryset = Repository.objects.all()
        filtering = {'name': ALL, 'affiliation': ALL}
        allowed_methods = ['get', 'post']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator

    def obj_create(self, bundle, request = None, **kwargs):
        get_repos(bundle.obj.github_token, bundle.obj.username)
        bundle.obj.data = {}
        return bundle


class ScoreResource(resources.MongoEngineResource):
    class Meta:
        queryset = Score.objects.all()
        allowed_methods = ['get', 'post']
        excludes = ['live_score']
        authentication = SessionAuthentication()
        authorization = AccountObjectsOnlyAuthorization()
        paginator_class = Paginator

    def obj_create(self, bundle, request = None, **kwargs):
        get_score(bundle.obj.username)
        bundle.obj.data = {}
        return bundle
