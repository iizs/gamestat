from django.core.management.base import BaseCommand, CommandError
from wget.models import Channel, PersistentQueue
from wget.utils import enqueue, dequeue, queue_stat

class Command(BaseCommand):
    help = 'Queue Test'
    args = 'enduque/dequeue queue_id (body)'

    def handle(self, *args, **options):
        if len(args) < 2 :
            raise CommandError('invalid arguments')

        if args[0] == 'enqueue':
            if len(args) < 3 :
                raise CommandError('invalid arguments')
            enqueue( args[1], args[2] )
        elif args[0] == 'dequeue':
            body = dequeue( args[1] )
            print body
        elif args[0] == 'stat':
            stats = queue_stat( args[1] )
            for k in stats:
                print "[{key}] {value}".format(key=k, value=stats[k])
        else:
            raise CommandError('invalid arguments')
