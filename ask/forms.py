from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ask.models import *

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}) )
    repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat password'}) )
    image = forms.ImageField(required=False)
'''
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username is already in use')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
            return email
        except ValidationError:
            raise forms.ValidationError('Invalid email')

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
	try:
           password = cleaned_data['password']
	except KeyError:
	   msg = 'Please enter your password twice!'
	   self._errors["password"] = self.error_class([msg])
	   return cleaned_data
	try:
	   repeat = cleaned_data['repeat']
	except KeyError:
	   msg = 'Please enter your password twice!'
	   self._errors["repeat"] = self.error_class([msg])
	   return cleaned_data
        if password != repeat:
            msg = 'Passwords didn`t match'
            self._errors["repeat"] = self.error_class([msg])
        return cleaned_data
'''
