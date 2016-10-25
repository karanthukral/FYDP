# routing.py
from channels.routing import route

channel_routing = [
         route('websocket.connect', 'nara_backend.consumers.ws_subscribe',
          path=r'^/traffic/(?P<topic>\w+)$'),
         ]
