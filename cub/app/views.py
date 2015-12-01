from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

from app.contribution import get_repos
from app.helpers import get_github_user_info
from app.models import Account
from app.oauth_github import ConnectGitHub


class Home(TemplateView):
    def get(self, request):
        return render(request, 'index.html', {})


class AuthorizeGitHubURL(View):

    def get(self, request):
        url = ConnectGitHub().authorize_url()
        return HttpResponseRedirect(url)


class AuthenticateGitHubAccount(View):

    def get(self, request):
        token = ConnectGitHub().get_access_token(request.GET['code'])
        github_user = get_github_user_info(token)
        account = Account.verify(github_user)
        request.message = AuthenticateGitHubAccount.login(
            request, account.username, account.github_token)
        return redirect("/")

    @classmethod
    def login(cls, request, username, github_token):
        user = authenticate(username=username, password=github_token)
        if user is not None:
            login(request, user)
            return {'message': "You successfully logged in."}
        else:
            return {'message': "Error logging you in."}



class LogoutGitHubAccount(View):

    def get(self, request):
        logout(request)
        return redirect("/")
