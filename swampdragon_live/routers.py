# -*- coding: utf-8 -*-
from swampdragon import route_handler
from swampdragon.route_handler import BaseRouter

class LiveTemplateRouter(BaseRouter):
    route_name = 'swampdragon-live'
    valid_verbs = ['subscribe', 'unsubscribe']

    def get_subscription_channels(self, key, **kwargs):
        if key.startswith('swampdragon-live-'):
            return [key]
        return []

route_handler.register(LiveTemplateRouter)
