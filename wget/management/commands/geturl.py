from django.core.management.base import BaseCommand, CommandError
from wget.models import Channel, PersistentQueue
from wget.models import QUEUE_FETCH_URL
from wget.utils import enqueue, dequeue, queue_stat

class Command(BaseCommand):
    help = 'schedule to get a web document'
    args = 'url'

    def handle(self, *args, **options):
        if len(args) < 1:
            raise CommandError('invalid arguments')

        enqueue( QUEUE_FETCH_URL, args[0] )

