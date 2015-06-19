from django.db import IntegrityError, transaction

import datetime
import time
import urllib2
import traceback
import importlib
import json

from models import Channel, PersistentQueue, PostProcessRule

QUEUE_FETCH_URL = 'wget.urls_to_fetch'
QUEUE_FETCHED_URL = 'wget.urls_fetched'
QUEUE_FAILED_URL = 'wget.urls_failed'
QUEUE_NO_POSTPROCESSOR = 'wget.no_postprocessor'
QUEUE_POSTPROCESS_FAILED = 'wget.postprocess_failed'

@transaction.atomic
def enqueue(channel_id, body):
    ch_list = Channel.objects.filter(channel_id = channel_id)
    if len(ch_list) == 0:
        ch = Channel(channel_id = channel_id)
        ch.save()
    else:
        ch = ch_list[0]

    q_obj = PersistentQueue(channel = ch, body = body)
    q_obj.save()

    ch.count_in +=1 
    ch.save()

@transaction.atomic
def dequeue(channel_id):
    try:
        ch = Channel.objects.get(channel_id = channel_id)
        if ch.count_in == ch.count_out:
            # nothing to dequeue
            return None

        q_list = PersistentQueue.objects.filter(channel = ch) \
                    .order_by('datetime')[:1]
        if len(q_list) == 0:
            # invalid state.
            # fix channel stat
            ch.count_out = ch.count_in
            ch.save()
            return None

        o = q_list[0]
        o.delete()
        ch.count_out += 1
        ch.save()

        return o.body

    except Channel.DoesNotExist as e:
        print 'invalid channel_id `{ch_id}`'.format(ch_id=channel_id)

def peep(channel_id):
    try:
        ch = Channel.objects.get(channel_id = channel_id)
        if ch.count_in == ch.count_out:
            # nothing to dequeue
            return None

        q_list = PersistentQueue.objects.filter(channel = ch) \
                    .order_by('datetime')[:1]
        if len(q_list) == 0:
            # invalid state.
            # but do not fix channel stat
            return None
        o = q_list[0]
        return o.body

    except Channel.DoesNotExist as e:
        print 'invalid channel_id `{ch_id}`'.format(ch_id=channel_id)

def queue_stat(channel_id):
    try:
        ch = Channel.objects.get(channel_id = channel_id)
        r = {}
        r['channel_id'] = ch.channel_id
        r['created_at'] =  ch.created_at
        r['count_in'] =  ch.count_in
        r['count_out'] =  ch.count_out
        r['size'] =  ch.count_in - ch.count_out

        return r
    except Channel.DoesNotExist as e:
        print 'invalid channel_id `{ch_id}`'.format(ch_id=channel_id)

def logger(msg):
    ts = datetime.datetime.now()
    print '[{ts}] {msg}'.format(ts=str(ts), msg=msg)

def enqueue_url(url):
    enqueue( QUEUE_FETCH_URL, url )

def fetch_url(sleep=1, autostop=600):
    last_successful_fetch = int(time.time())
   
    while ( autostop == 0 ) or ( autostop >= int(time.time()) - last_successful_fetch ) :
        url = dequeue(QUEUE_FETCH_URL)
        if url != None:
            body = {}
            body['url'] = url
            try:
                r = urllib2.urlopen(url)
                body['content'] = r.read()
                enqueue(QUEUE_FETCHED_URL, json.dumps(body))
                last_successful_fetch = int(time.time())
                logger('URL fetched; {url}'.format(url=url))
            except Exception as e:
                body['exception'] = traceback.format_exc()
                enqueue(QUEUE_FAILED_URL, json.dumps(body))
                logger('URL fetching failed; ' + body)
        else:
            remain = autostop - (int(time.time()) - last_successful_fetch)
            if remain < 60:
                msg = '; shutdown in {remain} seconds'.format(remain=remain)
            else:
                msg = ''

            logger('Queue empty{msg}'.format(msg=msg))

        time.sleep(sleep)

def postprocess_url(sleep=1, autostop=600):
    last_successful_process = int(time.time())

    while ( autostop == 0 ) or ( autostop >= int(time.time()) - last_successful_process ) :
        while True:
            body_json = dequeue(QUEUE_FETCHED_URL);
            if body_json == None:
                break

            try:
                body = json.loads(body_json)
                rule = PostProcessRule.get_rule(body['url'])
                rule.execute(body['content'])
                last_successful_process = int(time.time())
            except PostProcessRule.NoMatchingRuleFound as e:
                enqueue(QUEUE_NO_POSTPROCESSOR, json.dumps(body))
            except Exception as e:
                body['exception'] = traceback.format_exc()
                enqueue(QUEUE_POSTPROCESS_FAILED, json.dumps(body))
                logger('URL postprocess failed; ' + body['url'])

        remain = autostop - (int(time.time()) - last_successful_process)
        if remain < 60:
            msg = '; shutdown in {remain} seconds'.format(remain=remain)
        else:
            msg = ''

        logger('Queue empty{msg}'.format(msg=msg))
        time.sleep(sleep)

