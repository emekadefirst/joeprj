import firebase_admin
from firebase_admin import credentials, messaging


cred = credentials.Certificate('joseph-api-a63c5-eb2848002815.json')


firebase_admin.initialize_app(cred)
