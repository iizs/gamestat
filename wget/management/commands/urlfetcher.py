from django.core.management.base import BaseCommand, CommandError

from optparse import make_option

import datetime
import time
import urllib2
import traceback

from wget.models import Channel, PersistentQueue
from wget.models import QUEUE_FETCH_URL, QUEUE_FETCHED_URL, QUEUE_FAILED_URL
from wget.utils import enqueue, dequeue, queue_stat

class Command(BaseCommand):
    help = 'fetch web documents in queue'
    option_list = BaseCommand.option_list + (
        make_option('--sleep', 
            action='store', 
            type='int', 
            default=1, 
            dest='sleep', 
            help='sleeps SLEEP seconds after fetch a url'
        ),
        make_option('--auto-stop', 
            action='store', 
            type='int', 
            default=600, 
            dest='autostop', 
            help='stops AUTOSTOP seconds after last successful fetch'
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

        last_successful_fetch = int(time.time())
       
        while ( options['autostop'] == 0 ) or ( options['autostop'] >= int(time.time()) - last_successful_fetch ) :
            url = dequeue(QUEUE_FETCH_URL)
            if url != None:
                self.log('Fetching URL: {url}'.format(url=url))
                try:
                    r = urllib2.urlopen(url)
                    body = r.read()
                    enqueue(QUEUE_FETCHED_URL, body)
                    last_successful_fetch = int(time.time())
                    self.log('done')
                except Exception as e:
                    body = url + '\n'
                    body += traceback.format_exc()
                    enqueue(QUEUE_FAILED_URL, body)
                    self.log('failed; ' + body)
            else:
                remain = options['autostop'] - (int(time.time()) - last_successful_fetch)
                if remain < 60:
                    msg = '; shutdown in {remain} seconds'.format(remain=remain)
                else:
                    msg = ''

                self.log('Queue empty{msg}'.format(msg=msg))

            time.sleep(options['sleep'])
        
