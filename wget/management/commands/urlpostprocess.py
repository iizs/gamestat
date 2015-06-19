from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

from wget.utils import postprocess_url

class Command(BaseCommand):
    help = 'post process fetched url'
    option_list = BaseCommand.option_list + (
        make_option('--sleep', 
            action='store', 
            type='int', 
            default=1, 
            dest='sleep', 
            help='sleeps SLEEP seconds after process all urls'
        ),
        make_option('--auto-stop', 
            action='store', 
            type='int', 
            default=600, 
            dest='autostop', 
            help='stops AUTOSTOP seconds after last successful process'
        ),
    )

    def log(self, msg):
        ts = datetime.datetime.now()
        print '[{ts}] {msg}'.format(ts=str(ts), msg=msg)

    def handle(self, *args, **options):
        if options['sleep'] <= 0:
            raise CommandError('invalid arguments; SLEEP must be a positive integer')
        if options['autostop'] < 0:
            raise CommandError('invalid arguments; AUTOSTOP must be a positive integer')

        postprocess_url(
            sleep = options['sleep'],
            autostop = options['autostop'],
        )
