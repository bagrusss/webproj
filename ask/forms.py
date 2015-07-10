# -*- coding: utf-8 -*- 
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from ask.models import *

class SignUpForm(forms.Form):
    username = forms.CharField( label=u'Пользователь', max_length=30, 
				widget=forms.TextInput(attrs={'class':'form-control',
							      'placeholder':u'Пользователь'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control',
									  'placeholder':'Email'}))
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={'class':'form-control', 
								 'placeholder':u'Пароль'}) )
    repeat = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput(attrs={ 'class':'form-control', 
								'placeholder':u'Повторите пароль'}) )
    image = forms.ImageField(label=u'Фотография',required=False)

class AddQuestionForm(forms.Form):
    title=forms.CharField(label=u'Заголовок вопроса', max_length=100, 
				widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':u'Заголовок вопроса'}))
    text=forms.CharField(label=u'Текст вопроса', widget=forms.Textarea(attrs={'class':'form-control', 
						      'placeholder':u'Текст вопроса',
						      'id':'question_area'}))
    tags=forms.CharField(label=u'Тэги',
			 max_length=80,
			 widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':u'теги через запятую'}))


class AnswerForm(forms.Form):
    text=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 
						      'placeholder':u'Введите текст ответа',
						      'id':'answer_area'}))
'''
class SettingsForm(forms.Form):
    firstname=forms.CharField( label='First name',
				max_length=30, 
				widget=forms.TextInput(attrs={'class':'form-control',
							      'placeholder':'First name'}))
    secondname=forms.CharField( label='Second name',
				max_length=30, 
				widget=forms.TextInput(attrs={'class':'form-control',
							      'placeholder':'Second name'}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control',
									  'placeholder':'Email'}))'''



