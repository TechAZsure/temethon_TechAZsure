import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("path_to_your_firebase_json.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-firebase-db.firebaseio.com'
})