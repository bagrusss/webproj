# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ask.models import *

from django.core.paginator import Paginator
from django.http import Http404

import  datetime

def get_popular_tags(end):
    return Tag.objects.popular()[:end]

def index(request):
	a=request.GET.get('a','new')
	if a=='new':
           questions = Question.objects.new()[:20]
	   title='New Questions'
	if a=='pop':
	   questions =  Question.objects.popular()[0:20]
	   title='Popular Questions'
	if a=='tag':
	   tag=request.GET.get('tag','java')
	   title = 'Questions for tag "'+tag+'"'
	   questions =  Question.objects.get_questions_by_tag(tag)[0:20]
        poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:5]
        return render(request, 'index.html', {'questions':questions, 'title':title, 'poptags':poptags, 'popauthors':popauthors})

def signup(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:5]
	return render(request, 'signup.html', {'poptags':poptags, 'popauthors':popauthors})

def signin(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:5]
	if request.POST:
	   redirect = "/"
	   username=request.POST['username']
	   password=request.POST['password']
	   user = auth.authenticate(username=username, password=password)
	   if user is not None and user.is_active:
              auth.login(request, user)
              return HttpResponseRedirect(redirect)
	   else:
            return render(request, 'signin.html', {
                'poptags': poptags,
                'username': username,
                'password': password,
                'error': 1,
                'redirect': redirect
            })
	return render(request, 'signin.html', {'poptags':poptags, 'popauthors':popauthors})

def logout_v(request):
	logout(request)
	return HttpResponseRedirect("/")

def question(request):
	try:
	   q_id=int(request.GET.get('q'))
	except SyntaxError:
	   q_id=1
	except ValueError:
	   q_id=1
	except TypeError:
	   q_id=1
	question = Question.objects.get(id=q_id)
	tags = Tag.objects.tags_for_questions(q_id)
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:5]
	return render(request, 'question.html', {'question':question, 'tags':tags, 'poptags':poptags})


def addquestion(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:5]
	return render(request, 'addquestion.html', {'poptags':poptags, 'poptags':poptags})

def params(request):
	if request.method=='POST':
	   req = request.POST
	else:
	   req = request.GET
	keys=req.keys()
	res='hello\n'
	for key in keys:
	   res+='\n'+key+'='+req[key]
	return render(request, 'params.html',{'params':res})
