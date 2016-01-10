from github import Github

from backend.models import Repository, PRContribution, Score


def get_repos(account_github_token, account_username):
    """Save account public repositories data. """
    connection = Github(login_or_token=account_github_token, api_preview=True)
    repos = connection.get_user().get_repos()
    for repo in repos:

        if repo.raw_data['owner']['type'] == 'User':
            if repo.raw_data['owner']['login'] != account_username:
                repo.raw_data['affiliation'] = 'collaborator'
            else:
                repo.raw_data['affiliation'] = 'owner'
        else:
            repo.raw_data['affiliation'] = 'organization_member'

        Repository.create_or_update(repo.raw_data, account_username)


def get_pulls(account_github_token, account_username):
    """Save account merged pull requests. """
    connection = Github(login_or_token=account_github_token, api_preview=False)
    # Set query to find contributions
    qualifiers = {'is': 'merged', 'type': 'pr', 'author': account_username}
    pulls = connection.search_issues(
        query='', sort='updated', order='desc', **qualifiers)

    for pull in pulls:
        PRContribution.create_or_update(pull.raw_data, account_username)


def get_commits(account_username):
    pass


def get_score(account_username):
    return Score.compute(account_username)
