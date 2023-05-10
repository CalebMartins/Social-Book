from django import forms
from django.utils.translation import gettext_lazy as _
from authentication.models import Profile 

class SettingForm(forms.Form):
    profile_img = forms.ImageField(required=False, label='profile image')
    bio = forms.CharField(widget=forms.Textarea(), required=False)
    location = forms.CharField(max_length=100, required=False)