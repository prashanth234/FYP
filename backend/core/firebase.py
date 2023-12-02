import firebase_admin
from firebase_admin import credentials
import os

def intialize_firebase():
  cred = credentials.Certificate(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))
  firebase_admin.initialize_app(cred)