import time

from backend.contribution import get_repos, get_pulls, get_score, delete_repos
from backend.models.account import Account
from cub import celery_app
from cub.settings import CONTRIB_DELTA, MONGO_CONFIG


def get_contributions(account):
    get_repos(account.github_token, account.username)
    account.synced = int(time.time())
    account.save()

    delete_repos(account.github_token, account.username)
    account.synced = int(time.time())
    account.save()

    get_pulls(account.github_token, account.username)
    account.synced = int(time.time())
    account.save()

    get_score(account.username)
    account.synced = int(time.time())
    account.save()

    return account


@celery_app.task(name='get_all_contributions')
def get_all_contributions(account=None):
    sync = int(time.time()) - CONTRIB_DELTA
    if account:
        if account.synced <= sync:
            get_contributions(account)
        return account

    else:
        for account in Account.objects.filter(synced__lte=sync):
            get_contributions(account)
        return True
