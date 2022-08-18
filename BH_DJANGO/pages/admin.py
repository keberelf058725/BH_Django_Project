from django.contrib import admin
from .models import Nurse, Therapist, Flash_User, Admin
# Register your models here.

admin.site.register(Nurse)
admin.site.register(Therapist)
admin.site.register(Flash_User)
admin.site.register(Admin)