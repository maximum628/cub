import simplejson
from github import Github

from app.models import Repository

def get_repos(account):
        """Save account public repositories data. """
        connection = Github(login_or_token=account.github_token)
        repos = connection.get_user().get_repos(type='public')
        for repo in repos:
            Repository.create_or_update(repo.raw_data, account)
