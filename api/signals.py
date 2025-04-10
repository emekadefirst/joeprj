from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Program, DailyStudy
from .utils import send_push_notification

@receiver(post_save, sender=[Program, DailyStudy])
def notify_on_new_upload(sender, instance, created, **kwargs):
    if created:
        send_push_notification("New Data Study", "Check out the latest content in the app!")
