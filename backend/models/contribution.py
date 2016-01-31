import arrow
import mongoengine

from backend.models.abstract import AbstractContribution


class CommitContribution(AbstractContribution):

    files_stats = mongoengine.DictField()


class PRContribution(AbstractContribution):

    title = mongoengine.StringField(required=True)
    state = mongoengine.StringField(required=True)

    @classmethod
    def save_or_update(cls, raw_data, account):
        try:
            pr = PRContribution.objects.get(
                cub_account=account, html_url=raw_data['html_url'])

        except mongoengine.DoesNotExist:
            data = PRContribution.transform(account, raw_data)
            pr = PRContribution.save_document(data)
            return pr

        except mongoengine.MultipleObjectsReturned:
            pr = PRContribution.objects(
                    cub_account=account, html_url=raw_data['html_url'])[0]

        if (arrow.get(pr.updated_at) >=
                arrow.get(raw_data['updated_at'], 'YYYY-MM-DDTHH:mm:ss')):
            return pr

        data = PRContribution.transform(account, raw_data)
        pr = pr.update_document(data)
        return pr

    @classmethod
    def transform(cls, account, raw_data):
        data = {
            'cub_account': account,
            'html_url': raw_data['html_url'],
            'url': raw_data['url'],
            'html_repo_url': raw_data['html_url'].split('pull')[0],
            'updated_at': raw_data['updated_at'],
            'title': raw_data['title'],
            'state': raw_data['state']
        }
        return data
