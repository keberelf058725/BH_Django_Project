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

class Clinical_DC_Form(forms.Form):
    Start_Date = forms.DateField(label='Month Begin (inclusive)', required=True)
    End_Date = forms.DateField(label='Month End (exclusive)', required=True)
    ALOS_File = forms.FileField(label='ALOS File', required=True, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    DC_File = forms.FileField(label='Discharge Info File', required=True, validators=[FileExtensionValidator(allowed_extensions=['csv'])])
    Therapist = forms.FileField(label='Therapist List', required=True, validators=[FileExtensionValidator(allowed_extensions=['xlsx'])])


class Vivitrol_Form(forms.Form):
    Viv_File = forms.FileField(label='Vivitrol File', validators=[FileExtensionValidator(allowed_extensions=['csv'])])