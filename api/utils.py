from server.firebase import firebase_initialized
from firebase_admin import messaging
from .models import Device
import logging

logger = logging.getLogger(__name__)

def send_push_notification(title, body):
    if not firebase_initialized:
        logger.error("Firebase not initialized")
        return None

    try:
        devices = Device.objects.exclude(token__isnull=True).exclude(token__exact='')
        if not devices.exists():
            logger.warning("No valid devices found")
            return None

        results = []
        for device in devices:
            try:
                message = messaging.Message(
                    notification=messaging.Notification(
                        title=title,
                        body=body
                    ),
                    token=device.token
                )
                response = messaging.send(message)
                results.append({
                    'device_id': device.id,
                    'status': 'success',
                    'message_id': response
                })
                logger.info(f"Sent to device {device.id}")
            except Exception as e:
                results.append({
                    'device_id': device.id,
                    'status': 'error',
                    'error': str(e)
                })
                logger.error(f"Failed to send to device {device.id}: {str(e)}")

        return {
            'total': len(results),
            'success': sum(1 for r in results if r['status'] == 'success'),
            'results': results
        }

    except FirebaseError as e:
        logger.error(f"Firebase error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return None