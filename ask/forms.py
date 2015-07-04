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

