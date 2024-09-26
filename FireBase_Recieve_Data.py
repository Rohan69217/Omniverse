import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("C:/Users/Rohan/Downloads/omniverse-cloud-data-firebase-adminsdk-l44q9-f6adc414b5.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://omniverse-cloud-data-default-rtdb.firebaseio.com/'
})

ref = db.reference('accel')

def listener(event):
    print(f'Event type: {event.event_type}')
    print(f'Path: {event.path}')
    print(f'Value: {event.data}')

ref.listen(listener)
