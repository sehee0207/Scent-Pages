from django.db import models
from django.contrib.auth.models import User
from django.db.models import ImageField
from django.conf import settings

class Accounts(models.Model):
    profile_img = models.ImageField(upload_to = 'profile_pics', default='profile_pics/ha.jpg')
    
    def __str__(self):
        return "text : " + self.profile_img.url