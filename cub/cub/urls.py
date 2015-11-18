from django.conf.urls import include, url
from django.contrib import admin
from tastypie.api import Api

from app.api import AccountResource

v1_api = Api(api_name='v1')
v1_api.register(AccountResource())

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
]
