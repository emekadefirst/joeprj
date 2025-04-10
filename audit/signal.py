from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import AuditLog
from django.apps import apps
from datetime import datetime
from django.forms.models import model_to_dict

def serialize_datetime(value):
    if isinstance(value, datetime):
        return value.isoformat()  # This converts datetime to string
    return value

def get_changes(old, new):
    changes = {}
    for key in new:
        if old.get(key) != new.get(key):
            changes[key] = {'old': serialize_datetime(old.get(key)), 'new': serialize_datetime(new.get(key))}
    return changes

@receiver(post_save)
def model_save_handler(sender, instance, created, **kwargs):
    if sender.__name__ in ['AuditLog']:  # avoid recursion
        return

    user = getattr(instance, '_user', None)
    model_name = sender.__name__
    object_id = instance.pk
    new_data = model_to_dict(instance)

    if created:
        AuditLog.objects.create(
            user=user,
            model_name=model_name,
            object_id=object_id,
            action='CREATE',
            changes={'new': {key: serialize_datetime(val) for key, val in new_data.items()}}
        )
    else:
        try:
            old_instance = sender.objects.get(pk=object_id)
            old_data = model_to_dict(old_instance)
            changes = get_changes(old_data, new_data)
            if changes:
                AuditLog.objects.create(
                    user=user,
                    model_name=model_name,
                    object_id=object_id,
                    action='UPDATE',
                    changes=changes
                )
        except sender.DoesNotExist:
            pass

@receiver(post_delete)
def model_delete_handler(sender, instance, **kwargs):
    if sender.__name__ in ['AuditLog']:
        return

    user = getattr(instance, '_user', None)
    model_name = sender.__name__
    object_id = instance.pk
    old_data = model_to_dict(instance)

    AuditLog.objects.create(
        user=user,
        model_name=model_name,
        object_id=object_id,
        action='DELETE',
        changes={'old': {key: serialize_datetime(val) for key, val in old_data.items()}}
    )
