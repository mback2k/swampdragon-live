# -*- coding: utf-8 -*-
from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter
import hashlib

from .utils import get_channel_cache

class LiveTemplateRouter(BaseRouter):
    route_name = 'swampdragon-live'
    valid_verbs = ['subscribe', 'unsubscribe']

    def __init__(self, *args, **kwargs):
        self.channel_cache = get_channel_cache()
        return super(LiveTemplateRouter, self).__init__(*args, **kwargs)

    def get_subscription_channels(self, key, **kwargs):
        return self.channel_cache.keys('swampdragon-live-*')

    def subscribe(self, **kwargs):
        channel = kwargs.get('channel')
        if channel and self.validate_channel(channel):
            self.subscribe_valid_channel(channel)
        return super(LiveTemplateRouter, self).subscribe(**kwargs)

    def unsubscribe(self, **kwargs):
        channel = kwargs.get('channel')
        if channel and self.validate_channel(channel):
            self.unsubscribe_valid_channel(channel)
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

    def subscribe_valid_channel(self, channel):
        refc_cache_key = channel.replace('swampdragon-live-', 'swampdragon-live.refc.')
        if self.channel_cache.incr(refc_cache_key):
            self.channel_cache.expire(channel, timeout=300)

    def unsubscribe_valid_channel(self, channel):
        refc_cache_key = channel.replace('swampdragon-live-', 'swampdragon-live.refc.')
        if not self.channel_cache.decr(refc_cache_key):
            self.channel_cache.delete(channel)

route_handler.register(LiveTemplateRouter)
