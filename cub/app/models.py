from django.contrib.auth.hashers import make_password, check_password
import mongoengine

class Account(mongoengine.Document):

    meta = {
        'indexes': [{'fields': ['username', 'email']}]
    }

    username = mongoengine.StringField(required=True)
    github_token = mongoengine.StringField(required=True)
    name = mongoengine.StringField()
    email = mongoengine.EmailField(required=True)
    github_url = mongoengine.URLField(required=True)
    avatar_url = mongoengine.URLField()

    @classmethod
    def check(cls, data):
        if Account.objects.filter(username=data['username'], email=data['email']):
            account = Account.objects.get(username=data['username'], email=data['email'])

            if not check_password(data['github_token'], account.github_token):
                account.github_token = make_password(data['github_token'])
                account.save()
            return account
        else:
            return cls.create(data)

    @classmethod
    def create(cls, data):
        account = Account(
            username=data['username'], name=data['name'],
            email=data['email'], github_url=data['github_url'],
            avatar_url=data['avatar_url'])

        account.github_token = make_password(data['github_token'])
        account.save()
        return account

    @classmethod
    def authorize(cls, username, password):
        if Account.objects.filter(username=username):
            account = Account.objects.get(username=username)
            if check_password(password, account.github_token):
                return account
        return None


class Contribution(mongoengine.Document):
    meta = {
        'abstract': True,
        'indexes': [{'fields': ['account_id', 'created_date']}],
        'ordering': ['-created_date']
    }

    account_id = mongoengine.IntField(required=True)
    html_url = mongoengine.URLField(required=True)
    url = mongoengine.URLField(required=True)
    html_repo_url = mongoengine.URLField(required=True)
    repo_url = mongoengine.URLField(required=True)
    created_date = mongoengine.DateTimeField(required=True)
    stats = mongoengine.DictField()


class CommitContribution(Contribution):

    files_stats = mongoengine.DictField()


class PRContribution(Contribution):

    state = mongoengine.StringField(required=True)
