import arrow
import mongoengine

from backend.models.abstract import AbstractJSONDocument


class Repository(AbstractJSONDocument):

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
    def save_or_update(cls, raw_data, account):
        try:
            repo = Repository.objects.get(
                    cub_account=account, html_url=raw_data['html_url'])

        except mongoengine.DoesNotExist:
            data = Repository.transform(account, raw_data)
            repo = Repository.save_document(data)
            return repo

        except mongoengine.MultipleObjectsReturned:
            # should log the exception as a db inconsistency
            repo = Repository.objects.filter(
                    cub_account=account, html_url=raw_data['html_url'])[0]

        if (arrow.get(repo.updated_at) >=
                arrow.get(raw_data['updated_at'], 'YYYY-MM-DDTHH:mm:ss')):
            return repo

        data = Repository.transform(account, raw_data)
        repo = repo.update_document(data)
        return repo

    @classmethod
    def transform(cls, account, raw_data):

        if raw_data['owner']['type'] == 'User':
            if raw_data['owner']['login'] != account:
                raw_data['affiliation'] = 'collaborator'
            else:
                raw_data['affiliation'] = 'owner'
        else:
            raw_data['affiliation'] = 'organization_member'

        data = {
            'cub_account': account,
            'name': raw_data['name'],
            'description': raw_data['description'],
            'html_url': raw_data['html_url'],
            'url': raw_data['url'],
            'created_at': raw_data['created_at'],
            'updated_at': raw_data['updated_at'],
            'forks_count': raw_data['forks'],
            'fork': str(raw_data['fork']),
            'stargazers_count': raw_data['stargazers_count'],
            'watchers_count': raw_data['watchers_count'],
            'open_issues': raw_data['open_issues_count'],
            'affiliation': raw_data['affiliation']
        }
        return data
