from django.core.management.base import BaseCommand, CommandError

from wget.utils import enqueue_url

class Command(BaseCommand):
    help = 'schedule to get a web document'
    args = 'url'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('invalid arguments')

        enqueue_url(args[0])

