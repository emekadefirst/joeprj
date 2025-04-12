from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.forms.models import model_to_dict
from .models import AuditLog
from datetime import datetime

def serialize_datetime(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return value

def serialize_model(instance):
    data = {}
    for field in instance._meta.get_fields():
        if field.concrete and not field.many_to_many:
            value = getattr(instance, field.name)
            data[field.name] = serialize_datetime(value)
    return data

def get_changes(old, new):
    changes = {}
    for key in new:
        if old.get(key) != new.get(key):
            changes[key] = {
                'old': old.get(key),
                'new': new.get(key)
            }
    return changes

def is_audit_exempt(sender):
    return sender.__name__ in ['AuditLog'] or not hasattr(sender, '_meta') or not sender._meta.managed

@receiver(post_save)
def model_save_handler(sender, instance, created, **kwargs):
    if is_audit_exempt(sender):
        return

    user = getattr(instance, '_user', None)
    model_name = sender.__name__
    object_id = instance.pk
    new_data = serialize_model(instance)

    if created:
        AuditLog.objects.create(
            user=user,
            model_name=model_name,
            object_id=object_id,
            action='CREATE',
            changes={'new': new_data},
        )
    else:
        try:
            old_instance = sender.objects.get(pk=object_id)
            old_data = serialize_model(old_instance)
            changes = get_changes(old_data, new_data)
            if changes:
                AuditLog.objects.create(
                    user=user,
                    model_name=model_name,
                    object_id=object_id,
                    action='UPDATE',
                    changes=changes,
                )
        except sender.DoesNotExist:
            pass

@receiver(post_delete)
def model_delete_handler(sender, instance, **kwargs):
    if is_audit_exempt(sender):
        return

    user = getattr(instance, '_user', None)
    model_name = sender.__name__
    object_id = instance.pk
    old_data = serialize_model(instance)

    AuditLog.objects.create(
        user=user,
        model_name=model_name,
        object_id=object_id,
        action='DELETE',
        changes={'old': old_data},
    )
