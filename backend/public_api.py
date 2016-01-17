from tastypie import fields
from tastypie.constants import ALL
from tastypie.paginator import Paginator
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation
from tastypie_mongoengine import resources

from backend.forms import ContactForm
from backend.models import Account, Contact, Repository
from backend.authorization import ContactAuthorization

class AccountResource(ModelResource):
    class Meta:
        queryset = Account.objects.all()
        excludes = ['id', 'github_token', 'password', 'first_name', 'last_name',
                    'is_active', 'is_staff', 'is_superuser', 'email', 'date_joined',
                    'synced', 'last_login']
        filtering = {'username': ALL, 'name': ALL}
        allowed_methods = ['get']


class ContactResource(resources.MongoEngineResource):
    class Meta:
        queryset = Contact.objects.all()
        allowed_methods = ['post']
        authorization = ContactAuthorization()
        validation = FormValidation(form_class=ContactForm)


class RepositoryResource(resources.MongoEngineResource):
    class Meta:
        queryset = Repository.objects.all()
        excludes = ['updated_at', 'created_at', 'id', 'cub_account', 'url']
        filtering = {'name': ALL, 'affiliation': ALL}
        allowed_methods = ['get']
        paginator_class = Paginator
