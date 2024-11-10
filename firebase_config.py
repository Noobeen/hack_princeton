import firebase_admin
from firebase_admin import credentials, auth, firestore

# Initialize Firebase
cred = credentials.Certificate("C:\\Users\\DELL\\Desktop\\myproject\\serviceAccountKey.json")

firebase_admin.initialize_app(cred)

# Firestore Database and Auth
db = firestore.client()