from django.core.management.base import BaseCommand, CommandError

from backend.models.account import Account
from backend.tasks import get_all_contributions

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--username', dest='username', default=None)

    def handle(self, *args, **options):
        if options.get('username'):
            username = options.get('username')
            try:
                account = Account.objects.get(username=username)
            except Account.DoesNotExist:
                raise CommandError('Account "%s" does not exist' % username)

            get_all_contributions(account)
            self.stdout.write(
                    'Successfully fetched all user  "%s" contributions' % username)
        else:
            get_all_contributions()
            self.stdout.write('Successfully fetched all users contributions')
