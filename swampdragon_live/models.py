# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import push_new_content

@receiver(post_save)
def post_save_handler(sender, instance, **kwargs):
    if ContentType.objects.exists():
        instance_type = ContentType.objects.get_for_model(instance.__class__)

        push_new_content.apply_async(countdown=1, kwargs={'instance_type_pk': instance_type.pk,
                                                          'instance_pk': instance.pk})
