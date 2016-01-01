from tastypie.authorization import Authorization
from tastypie.exceptions import Unauthorized


class AccountObjectsOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(cub_account=bundle.request.user.username)

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user


class AccountOnlyAuthorization(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.all()

    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

    def update_list(self, object_list, bundle):
        allowed = []

        # Since they may not all be saved, iterate over them.
        for obj in object_list:
            if obj.user == bundle.request.user:
                allowed.append(obj)

        return allowed

    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
