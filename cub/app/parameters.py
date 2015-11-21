import os

# GitHub
DEFAULT_TIMEOUT = 30
DEFAULT_USER_AGENT = 'PyGithub/Python'
GITHUB_BASE_URL = 'https://github.com'
GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
