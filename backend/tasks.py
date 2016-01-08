import time

from backend.contribution import get_repos, get_pulls, get_live_score
from backend.models import Account
from cub.settings import CONTRIB_DELTA


def get_contributions(account):
    get_repos(account.github_token, account.username)
    account.synced = int(time.time())
    account.save()

    get_pulls(account.github_token, account.username)
    account.synced = int(time.time())
    account.save()

    get_live_score(account.username)
    account.synced = int(time.time())
    account.save()

    return account


def get_all_contributions(account=None):
    sync = int(time.time()) - CONTRIB_DELTA
    if account:
        if account.synced <= sync:
            get_contributions(account)
        else:
            return account
    else:
        for account in Account.objects.filter(synced__lte=sync):
            get_contributions(account)
