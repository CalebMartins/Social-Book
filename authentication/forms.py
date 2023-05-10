from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data):
            raise forms.ValidationError(_('This email already exists'))
        
        return data
    
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if confirm_password != password:
            raise forms.ValidationError(_('Both password fields don\'t match'))
        
        return confirm_password

class SignInForm(forms.Form):
    Usermail = forms.CharField(label='Username or Email')
    Password = forms.CharField(widget=forms.PasswordInput)
