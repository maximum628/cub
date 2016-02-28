from github import Github

from backend.models.contribution import CommitContribution, PRContribution
from backend.models.repository import Repository
from backend.models.score import  Score


def get_repos(account_github_token, account_username):
    """Save account public repositories data. """
    connection = Github(login_or_token=account_github_token, api_preview=True)
    repos = connection.get_user().get_repos()

    for repo in repos:
        Repository.save_or_update(repo.raw_data, account_username)


def delete_repos(account_github_token, account_username):
    """ Delete from database repos that are not in GitHub """
    connection = Github(login_or_token=account_github_token, api_preview=True)

    github_repos = connection.get_user().get_repos()

    gh_repos = set([r.raw_data['name'] for r in github_repos])
    db_repos = set(Repository.objects.filter(
            cub_account=account_username).values_list('name'))

    repos_to_delete = db_repos - gh_repos
    for db_repo in repos_to_delete:
        Repository.objects.get(name=db_repo).delete()


def get_pulls(account_github_token, account_username):
    """Save account merged pull requests. """
    connection = Github(login_or_token=account_github_token, api_preview=False)
    # Set query to find contributions
    qualifiers = {'is': 'merged', 'type': 'pr', 'author': account_username}
    pulls = connection.search_issues(
        query='', sort='updated', order='desc', **qualifiers)

    for pull in pulls:
        PRContribution.save_or_update(pull.raw_data, account_username)


def get_commits(account_username):
    pass


def get_score(account_username):
    return Score.compute(account_username)
