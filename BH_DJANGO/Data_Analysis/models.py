from django.db import models

class Vivtrol_Analyzer(models.Model):
    title = models.CharField(max_length=120)
    field_2 = models.FileField(name= 'File to Be Uploaded')

#this is object data stored in db