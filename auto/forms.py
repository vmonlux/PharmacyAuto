from django import forms
from django.forms import ModelForm
from django.forms.fields import Field
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from auto.models import *

class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom attributes to fields, e.g., placeholders
        self.fields['new_password1'].widget.attrs['placeholder'] = 'New Password'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm New Password'


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            'email',
            'first_name',
            'last_name',
            'is_staff'
        )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'last_name',
            'is_staff'
        )

class OmnicellCreateForm(ModelForm):
    class Meta:
        model = Omnicell
        fields = ['Omni_Id', 'Serial_Number', 'Omni_Description', 'Emergency', 'Model', 'CT_Version', 'PC_Name', 'Ivanti', 'Port_Name', 'Port_Location', 'Site', 'Building', 'Boom', 'Area', 'Room', 'Door_Code', 'Note']
        widgets = {
            'Serial_Number': forms.TextInput(attrs={'class': 'inputField'}),
        }

class OmnicellForm(ModelForm):
    class Meta:
        model = Omnicell
        fields = ['Serial_Number', 'Omni_Description', 'Emergency', 'Model', 'CT_Version', 'PC_Name', 'Ivanti', 'Port_Name', 'Port_Location', 'Site', 'Building', 'Boom', 'Area', 'Room', 'Door_Code', 'Note', 'Org', 'HD_Type']
        widgets = {
            'Serial_Number': forms.TextInput(attrs={'class': 'inputField'}),
        }

class AuxForm(ModelForm):
    class Meta:
        model = Aux
        fields = ['Omnicell', 'Serial_Number', 'Model']

class LockboxForm(ModelForm):
    class Meta:
        model = Lockbox
        fields = ['Refrigerator', 'Medication', 'Key', 'Description']
        
class RefrigeratorCreateForm(ModelForm):
    class Meta:
        model = Refrigerator
        fields = ['Facilities_Id', 'Omnicell', 'Model']
        widgets = {
            'Facilities_Id': forms.TextInput(attrs={'class': 'inputField'}),
        }

class RefrigeratorForm(ModelForm):
    class Meta:
        model = Refrigerator
        fields = ['Facilities_Id', 'Omnicell', 'Model']
        widgets = {
            'Facilities_Id': forms.TextInput(attrs={'class': 'inputField'}),
        }
        
class ServiceItemForm(ModelForm):
    class Meta:
        model = ServiceItem
        fields = ('__all__')


