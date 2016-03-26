# -*- coding: utf-8 -*-
from django.core.cache import InvalidCacheBackendError, caches
from django.core.cache.utils import make_template_fragment_key
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
    
            fragment_name = hashlib.sha1(tag_name + template_name).hexdigest()
            user_cache_key = make_template_fragment_key(fragment_name, [user.id,
                                                                        instance_type.pk,
                                                                        instance.pk])
            user_cache_key = user_cache_key.replace('.', '_')
            user_cache_keys.append(user_cache_key)
            channel_cache.set(user_cache_key, (template_name, new_context))
    
            cache_key = make_template_fragment_key('swampdragon-live', [instance_type.pk,
                                                                        instance.pk])
            cache_keys = channel_cache.get(cache_key, set())
            cache_keys.add(user_cache_key)
            channel_cache.set(cache_key, set(cache_keys))

    channels = map(lambda c: 'swampdragon-live-%s' % c, user_cache_keys)
    classes = 'swampdragon-live %s' % ' '.join(channels)

    content = '<%s class="%s">' % (tag_name, classes)
    content += get_template(template_name).render(new_context)
    content += '</%s>' % tag_name
    return content
