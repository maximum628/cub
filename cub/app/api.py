from tastypie.resources import ModelResource
from app.models import Account


class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        allowed_methods = ['get']
