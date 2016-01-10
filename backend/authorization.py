from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class AccountObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(cub_account=bundle.request.user.username)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def create_list(self, object_list, bundle):
        return object_list

    def create_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class AccountOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.all()

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class MyAccountOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(username=bundle.request.user.username)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class ContactAuthorization(Authorization):
    def post_list(self, object_list, bundle):
        return True

    def post_detail(self, object_list, bundle):
        return True
