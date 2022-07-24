from django import forms
from django.core.validators import FileExtensionValidator

class Flash_File_Form(forms.Form):
    Flash_File = forms.FileField(label='Flash File', validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])
    Kipu_File = forms.FileField(label='Kipu File', validators=[FileExtensionValidator(allowed_extensions=['csv'])])

"""    def clean_Flash_File(self,*agrs, **kwargs):
        Flash_File = self.cleaned_data.get("Flash_File")
        if "*.xlsx" in Flash_File:
            return Flash_File
        else:
            raise forms.ValidationError("Not Valid File")"""
