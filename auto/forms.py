from django import forms
from django.forms import ModelForm
from django.forms.fields import Field
from auto.models import *

class OmnicellForm(ModelForm):
    class Meta:
        model = Omnicell
        fields = ['Serial_Number', 'Omni_Description', 'Emergency', 'Model', 'CT_Version', 'PC_Name', 'Ivanti', 'Site', 'Building', 'Area', 'Room', 'Door_Code', 'Note']
        widgets = {
            'Serial_Number': forms.TextInput(attrs={'class': 'inputField'}),
        }

class AuxForm(ModelForm):
    class Meta:
        model = Aux
        fields = ['Omnicell', 'Serial_Number', 'Model']
        
class RefrigeratorForm(ModelForm):
    class Meta:
        model = Refrigerator
        fields = ['Facilities_Id', 'Type', 'Omnicell']
        widgets = {
            'Facilities_Id': forms.TextInput(attrs={'class': 'inputField'}),
        }