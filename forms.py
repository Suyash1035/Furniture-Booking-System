from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from . models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control','class':'form-label', 'class':'w-75 mx-auto mb-4'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control','class':'form-label','class':'w-75 mx-auto mb-4'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control','class':'form-label','class':'w-75 mx-auto mb-4'}))

    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        labels = {'email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control','class':'form-label','class':'w-75 mx-auto mb-4'})}

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-control','class':'form-label','class':'w-75 mx-auto mb-4'}))
    password = forms.CharField(label='Password',strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'currentpassword','class':'form-control','class':'form-label','class':'w-75 mx-auto mb-4'}))

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':'True','class':'form-control'}))
    new_password1 = forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=500,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
   
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','class':'w-100  mb-4'}),help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm Password'),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control','class':'w-100 mb-4'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'locality' : forms.TextInput(attrs={'class':'form-control'}),
            'city' : forms.TextInput(attrs={'class':'form-control'}),
            'state' : forms.Select(attrs={'class':'form-control'}),
            'zipcode' : forms.NumberInput(attrs={'class':'form-control'}),
        }

