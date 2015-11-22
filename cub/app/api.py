from tastypie_mongoengine import resources

from app.models import Account, CommitContribution


class AccountResource(resources.MongoEngineResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['github_token', 'id']
        allowed_methods = ['get']


class CommitContributionResource(resources.MongoEngineResource):
    class Meta:
        queryset = CommitContribution.objects.all()
        allowed_methods = ['get']
