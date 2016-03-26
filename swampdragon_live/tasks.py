# -*- coding: utf-8 -*-
from swampdragon.pubsub_providers.data_publisher import publish_data
from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.utils import make_template_fragment_key
from django.template.loader import get_template
from celery.task import task

@task(ignore_result=True)
def push_new_content(instance_type_pk, instance_pk):
    try:
        channel_cache = caches['swampdragon-live']
    except InvalidCacheBackendError:
        channel_cache = caches['default']

    cache_key = make_template_fragment_key('swampdragon-live', [instance_type_pk,
                                                                instance_pk])
    cache_keys = channel_cache.get(cache_key, [])

    for cache_key in cache_keys:
        template_name, new_context = channel_cache.get(cache_key, (None, None))
        if template_name and new_context:
            channel = 'swampdragon-live-%s' % cache_key
            value = get_template(template_name).render(new_context)
            publish_data(channel=channel, data=value)
