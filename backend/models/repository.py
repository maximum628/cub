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
        data = Repository.transform(raw_data)
        data['cub_account'] = account

        if Repository.objects(
                cub_account=account, html_url=data['html_url']):

            repo = Repository.objects.get(
                    cub_account=account, html_url=data['html_url'])
            repo = repo.update_document(data)

        else:
            repo = Repository.save_document(data)

        return repo

    @classmethod
    def transform(cls, raw_data):
        data = {
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
