# consumers.py

import logging

from channels import Group
from channels.sessions import channel_session

logger = logging.getLogger(__name__)

@channel_session
def ws_subscribe(message, topic):
    Group(topic).add(message.reply_channel)
    message.channel_session['topic'] = topic
