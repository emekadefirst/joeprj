from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Program, DailyStudy
from .utils import send_push_notification  

@receiver(post_save, sender=Program)
def notify_on_new_program(sender, instance, created, **kwargs):
    if created:
        send_push_notification("New Program Created", f"Check out the new program: {instance.title}")

@receiver(post_save, sender=DailyStudy)
def notify_on_new_daily_study(sender, instance, created, **kwargs):
    if created:
        send_push_notification("New Daily Study Added", f"Check out the new daily study: {instance.title}")
