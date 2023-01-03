from django.db import models
from django.conf import settings

from Category import *
from Competation import *

class Post(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.OneToOneField(Category, on_delete=models.CASCADE)
    competation = models.OneToOneField(Competation, on_delete=models.CASCADE)
    
class PostImage(models.Model):
    image = models.FileField(upload_to="files")
    post = models.ForeignKey(Post, on_delete=models.CASCADE)