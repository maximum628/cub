from github import Github

def get_github_user_info(token):
    connection = Github(login_or_token=token).get_user()
    return {'email': connection.email, 'name': connection.name,
            'github_url': connection.html_url, 'github_token': token,
            'avatar_url': connection.avatar_url,
            'username': connection.html_url.split('/')[-1]}
