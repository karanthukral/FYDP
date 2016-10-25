# signals.py

import logging

from json import dumps

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from channels import Group

from nara_backend.models import Traffic

logger = logging.getLogger(__name__)

def send_update(update, topic):
    logger.info('send_update called with update = %s and topic = %s', update,
            topic)
    Group(topic).send({'data': dumps(update)})

@receiver(post_save, sender=Traffic)
def traffic_post_save(sender, instance, **kwargs):
    send_update({
        'name': instance.human_identifier,
        'created_date': instance.created_date,
        'flagged': instance.flagged,
        'metadata': instance.metadata
        }, 'traffic'
        )
