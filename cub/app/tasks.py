from app.contribution import get_repos, get_pulls, get_live_score

def get_contributions(account_github_token, account_username):
    get_repos(account_github_token, account_username)
    get_pulls(account_github_token, account_username)
    get_live_score(account_username)
