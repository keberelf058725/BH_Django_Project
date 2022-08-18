from django.db import models

from django.contrib.auth.models import User

class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Nurse = models.BooleanField(default=False,null=True, blank=True)

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Therapist = models.BooleanField(default=False,null=True, blank=True)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Admin = models.BooleanField(default=False,null=True, blank=True)

class Flash_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Flash = models.BooleanField(default=False,null=True, blank=True)