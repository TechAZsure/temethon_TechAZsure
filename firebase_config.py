import firebase_admin
from firebase_admin import credentials, db

# Initialize the Firebase app with your service account and database URL
if not firebase_admin._apps:
    cred = credentials.Certificate("temenos-techazsure.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://temenos-techazsure-default-rtdb.asia-southeast1.firebasedatabase.app/'
    })
