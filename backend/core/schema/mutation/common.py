from entity.models.Entity import Entity
from core.models.User import User
from entity.schema.query.userEntityQuery import UserEntityCheck
from django.utils.translation import gettext as _

def verify_entity(entity):
  try:
    entity = Entity.objects.get(key=entity, ispublic=True)
  except Entity.DoesNotExist:
    return {
      "success": False, 
      "errors": {
        "message": _("Entity doesn't exist."),
        "code": "entity_not_found"
      }
    }
  
  return {"success": True, "entity": entity}

def verify_user(username):
  try:
    user = User.objects.get(username=username)
  except User.DoesNotExist:
    return {
      "success": False, 
      "errors": {
        "message": _("User doesn't exist"),
        "code": "access_denied"
      }
    }
  
  return {"success": True, "user": user}

def verify_entity_access(user, entity):
  if not UserEntityCheck.has_access(user=user, entity_id=entity.id):
    return {
      "success": False, 
      "errors": {
        "message": _("No access"),
        "code": "access_denied"
      }
    }
  
  return {"success": True}