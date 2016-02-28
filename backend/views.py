from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import View, TemplateView

from backend.helpers import get_github_user_info
from backend.models.account import Account
from backend.oauth_github import ConnectGitHub
from backend.tasks import get_all_contributions


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


class Contributions(View):

    def get(self, request):
        account = Account.objects.get(username=request.user.username)
        get_all_contributions.delay(account)
        return redirect('/')
