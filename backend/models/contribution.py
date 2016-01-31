import mongoengine

from backend.models.abstract import AbstractContribution


class CommitContribution(AbstractContribution):

    files_stats = mongoengine.DictField()


class PRContribution(AbstractContribution):

    title = mongoengine.StringField(required=True)
    state = mongoengine.StringField(required=True)

    @classmethod
    def save_or_update(cls, raw_data, account):
        data = PRContribution.transform(raw_data)
        data['cub_account'] = account

        if PRContribution.objects(
                cub_account=account, html_url=data['html_url']):

            pr = PRContribution.objects.get(
                    cub_account=account, html_url=data['html_url'])
            pr = pr.update_document(data)

        else:
            pr = PRContribution.save_document(data)

        return pr

    @classmethod
    def transform(cls, raw_data):
        data = {
            'html_url': raw_data['html_url'],
            'url': raw_data['url'],
            'html_repo_url': raw_data['html_url'].split('pull')[0],
            'updated_at': raw_data['updated_at'],
            'title': raw_data['title'],
            'state': raw_data['state']
        }
        return data
