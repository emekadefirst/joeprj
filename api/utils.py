from .models import Device
from server import firebase
from firebase_admin import messaging

def send_push_notification(title, body):
    tokens = Device.objects.values_list('token', flat=True)
    if not tokens:
        return None
        
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        tokens=list(tokens)
    )
    
    try:
        response = messaging.send_multicast(message)
        return response
    except Exception as e:
        print(f"Error sending notification: {e}")
        return None