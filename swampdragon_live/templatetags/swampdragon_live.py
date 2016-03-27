# -*- coding: utf-8 -*-
from django.core.cache import InvalidCacheBackendError, caches
from django.contrib.contenttypes.models import ContentType
from django.template.loader import get_template
from django.template import Context, Library
from django.db.models import Model
import hashlib

register = Library()

@register.simple_tag(takes_context=True)
def include_live(context, tag_name, template_name, **kwargs):
    user = context['user']
    new_context = Context(kwargs)

    try:
        channel_cache = caches['swampdragon-live']
    except InvalidCacheBackendError:
        channel_cache = caches['default']

    user_cache_keys = []
    for value in kwargs.values():
        if isinstance(value, Model):
            instance = value
            instance_type = ContentType.objects.get_for_model(instance.__class__)
    
            fragment_hash = hashlib.sha1('%s:%s' % (tag_name, template_name)).hexdigest()
            instance_hash = hashlib.sha1('%d:%d' % (instance_type.pk, instance.pk)).hexdigest()
            username_hash = hashlib.sha1('%d:%s' % (user.id, user.username)).hexdigest()
            user_cache_key = '%s-%s-%s' % (fragment_hash, instance_hash, username_hash)
            user_cache_keys.append(user_cache_key)
            channel_cache.set(user_cache_key, (template_name, new_context))
    
            cache_key = 'swampdragon-live.type.%d.instance.%d' % (instance_type.pk, instance.pk)
            cache_keys = channel_cache.get(cache_key, set())
            cache_keys.add(user_cache_key)
            channel_cache.set(cache_key, set(cache_keys))

    channels = map(lambda c: 'swampdragon-live-%s' % c, user_cache_keys)
    classes = 'swampdragon-live %s' % ' '.join(channels)

    content = '<%s class="%s">' % (tag_name, classes)
    content += get_template(template_name).render(new_context)
    content += '</%s>' % tag_name
    return content
