# -*- coding: utf-8 -*-
from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
import hashlib

from .utils import get_channel_cache

class LiveTemplateRouter(BaseRouter):
    route_name = 'swampdragon-live'
    valid_verbs = ['subscribe', 'unsubscribe']
    valid_channels = {}

    def get_subscription_channels(self, key, **kwargs):
        return self.valid_channels.keys()

    def subscribe(self, **kwargs):
        channel = kwargs.get('channel')
        if channel and self.validate_channel(channel):
            self.valid_channels.setdefault(channel, channel)
            self.update_channel(channel)
        return super(LiveTemplateRouter, self).subscribe(**kwargs)

    def unsubscribe(self, **kwargs):
        channel = kwargs.get('channel')
        if channel and self.validate_channel(channel):
            self.valid_channels.pop(channel, channel)
            self.delete_channel(channel)
        return super(LiveTemplateRouter, self).unsubscribe(**kwargs)

    def validate_channel(self, channel):
        if channel.startswith('swampdragon-live-'):
            user = self.connection.get_user()
            if user:
                username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
                if username_hash:
                    if channel.split('-')[-1] == username_hash:
                        return True
        return False

    def update_channel(self, channel):
        channel_cache = get_channel_cache()
        data = channel_cache.get(channel)
        if not data is None:
            channel_cache.set(channel, data)

    def delete_channel(self, channel):
        channel_cache = get_channel_cache()
        channel_cache.delete(channel)

route_handler.register(LiveTemplateRouter)
