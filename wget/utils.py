from django.db import IntegrityError, transaction

from models import Channel, PersistentQueue

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
