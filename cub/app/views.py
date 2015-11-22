from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.generic import View

from app.helpers import get_github_user_info
from app.models import Account
from app.oauth_github import ConnectGitHub


class AuthorizeGitHubURL(View):

    def get(self, request):
        url = ConnectGitHub().authorize_url()
        return HttpResponseRedirect(url)


class AuthenticateGitHubAccount(View):

    def get(self, request):
        token = ConnectGitHub().get_access_token(request.GET['code'])
        github_user = get_github_user_info(token)
        account = Account.check(github_user)
        message = self.login(request, account)
        return redirect("/")

    def login(self, request, account):
        user = Account.authorize(
            username=account.username, password=account.github_token)
        if user is not None:
            login(request, user)
            return {'message': "Account successfully logged in."}
        else:
            return {'message': "Error logging user in."}

class LogoutGitHubAccount(View):

    def get(self, request):
        logout(request)
        return redirect("/")
