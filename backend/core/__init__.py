from core.firebase import intialize_firebase
import sys

if 'collectstatic' not in sys.argv:
  intialize_firebase()