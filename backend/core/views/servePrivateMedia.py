import os
from django.conf import settings
from django.http import HttpResponse, Http404, HttpResponseForbidden

from graphql_jwt.backends import JSONWebTokenBackend

def serve_private_media(request, path):
  user = JSONWebTokenBackend().authenticate(request)

  if not user or f'user_{user.id}' != path.split('/')[1]:
    return HttpResponseForbidden('Forbidden')
  
  file_path = os.path.join(settings.MEDIA_ROOT, 'private', path)
  
  if os.path.exists(file_path):
    extension = os.path.splitext(file_path)[1][1:]
    with open(file_path, 'rb') as file:
      response = HttpResponse(file.read(), content_type=f"image/{extension}")
      return response
  else:
    raise Http404