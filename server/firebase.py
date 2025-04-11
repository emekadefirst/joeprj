import firebase_admin
from firebase_admin import credentials, messaging
from firebase_admin.exceptions import FirebaseError

def initialize_firebase():
    try:
        # Make sure the path to your JSON file is correct
        cred = credentials.Certificate('joseph-api-a63c5-eb2848002815.json')
        
        # Verify the project ID matches your JSON file
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred, {
                'projectId': 'joseph-api-a63c5',
                'storageBucket': 'joseph-api-a63c5.appspot.com'
            })
        return True
    except Exception as e:
        print(f"Firebase initialization failed: {str(e)}")
        return False

# Initialize immediately when module loads
firebase_initialized = initialize_firebase()