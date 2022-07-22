from django.db import models

from django.contrib.auth.models import User

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.BooleanField(default=False)
