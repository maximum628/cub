from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from app.api import (AccountResource, CommitContributionResource,
    PRContributionResource, RepositoryResource, ScoreResource)
from app.views import (AuthorizeGitHubURL, AuthenticateGitHubAccount,
    LogoutGitHubAccount, Home, Contributions)

v1_api = Api(api_name='v1')
v1_api.register(AccountResource())
v1_api.register(CommitContributionResource())
v1_api.register(PRContributionResource())
v1_api.register(RepositoryResource())
v1_api.register(ScoreResource())


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^authorize/', AuthorizeGitHubURL.as_view(), name='authorize'),
    url(r'^authenticate/', AuthenticateGitHubAccount.as_view(), name='authenticate'),
    url(r'^logout/', LogoutGitHubAccount.as_view(), name='logout'),
    url(r'^contribution/', Contributions.as_view(), name='contrib'),
    url(r'^[\w]*', Home.as_view(), name='home'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
