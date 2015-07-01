# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ask.models import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

import  datetime

authors=5

def get_popular_tags(end):
    return Tag.objects.popular()[:end]

actions=frozenset({'new','pop','tag'})

def index(request):
	a=request.GET.get('a','new')
	if a not in actions:
	   raise Http404
	questions_list=0;
	if a=='new':
           questions_list = Question.objects.new()
	   title='New Questions'
	if a=='pop':
	   questions_list =  Question.objects.popular()
	   title='Popular Questions'
	if a=='tag':
	   tag=request.GET.get('tag','java')
	   title = 'Questions for tag "'+tag+'"'
	   questions_list = Question.objects.get_questions_by_tag(tag)
	page = request.GET.get('page',1)
	paginator=Paginator(questions_list, 2)
	try:
	   questions=paginator.page(page)
	except PageNotAnInteger:
	   questions=paginator.page(1)
	except EmptyPage:
	   raise Http404 #questions=paginator.page(paginator.num_pages)
	
        poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
        return render(request, 'index.html', {	'questions':questions, 
						'title':title, 
						'poptags':poptags, 
						'popauthors':popauthors,
						'a':a})

def signup(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
	return render(request, 'signup.html', {'poptags':poptags, 'popauthors':popauthors})

def signin(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
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
                'error': 1,
                'redirect': redirect
            })
	return render(request, 'signin.html', {'poptags':poptags, 'popauthors':popauthors})

def logout_v(request, page=1):
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
	answers_list=question.answer_set.all()
	tags = Tag.objects.tags_for_questions(q_id)
	poptags = get_popular_tags(10)
	page = request.GET.get('page', 1)
	paginator=Paginator(answers_list, 2)
	answers=0
	try:
	   answers=paginator.page(page)
	except PageNotAnInteger:
	   answers=paginator.page(1)
	except EmptyPage:
	   raise Http404 #answers=paginator.page(paginator.num_pages)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
	return render(request, 'question.html', {'question':question, 
						 'tags':tags, 
						 'poptags':poptags, 
						 'answers':answers, 
						 'popauthors':popauthors, 
						 'page':page,
						 'q':q_id})

def addquestion(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
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
