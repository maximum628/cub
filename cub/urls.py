from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api

from backend import api
from backend import public_api
from backend.views import (AuthorizeGitHubURL, AuthenticateGitHubAccount,
    LogoutGitHubAccount, Home, Contributions)

v1_api = Api(api_name='v1')
v1_api.register(api.AccountResource())
v1_api.register(api.MyAccountResource())
v1_api.register(api.CommitContributionResource())
v1_api.register(api.PRContributionResource())
v1_api.register(api.RepositoryResource())
v1_api.register(api.ScoreResource())

pub_api = Api(api_name='public')
pub_api.register(public_api.AccountResource())
pub_api.register(public_api.ContactResource())
pub_api.register(public_api.RepositoryResource())

urlpatterns = static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/', include(pub_api.urls)),
    url(r'^authorize/', AuthorizeGitHubURL.as_view(), name='authorize'),
    url(r'^authenticate/', AuthenticateGitHubAccount.as_view(), name='authenticate'),
    url(r'^logout/', LogoutGitHubAccount.as_view(), name='logout'),
    url(r'^contribution/', Contributions.as_view(), name='contrib'),
    url(r'^djangojs/', include('djangojs.urls')),
    # Leave it last
    url(r'^[\w]*', Home.as_view(), name='home')
]
