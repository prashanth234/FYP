from core.firebase import intialize_firebase
from django.conf import settings
import sys

if settings.ENABLE_FIREBASE and 'collectstatic' not in sys.argv:
  intialize_firebase()