# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from ask.forms import *

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError

import  datetime

authors=5
uname='username'
passw='password'

def get_popular_tags(end):
    return Tag.objects.popular()[:end]

def signin(request):
	if request.user.is_authenticated():
           return HttpResponseRedirect('/')
	poptags = get_popular_tags(10)
	next=request.GET.get('next')
	popauthors = Profile.objects.get_queryset().order_by('-rating')[:authors]	
	if request.POST:
	   username=request.POST[uname]
	   password=request.POST[passw]
	   user = auth.authenticate(username=username, password=password)
	   if user is not None and user.is_active:
              auth.login(request, user)
              return HttpResponseRedirect(next)
	   else:
              return render(request, 'signin.html', {
                'poptags': poptags,
                'username': username,
                'error': 1,
                'redirect': redirect
            	})
	return render(request, 'signin.html', {'poptags': poptags,
						'popauthors':popauthors,
						'next': next})

def signup(request):
	if request.user.is_authenticated():
           return HttpResponseRedirect("/")
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
	form = SignUpForm()
	if request.POST:
	   form = SignUpForm(request.POST, request.FILES)
	   if form.is_valid():
	      	passw = form.cleaned_data['password']
		repeat = form.cleaned_data['repeat']		
		if repeat == passw:
		   user = form.cleaned_data['username']
		   email = form.cleaned_data['email']
		   u = User.objects.create_user(username=user, email=email)
		   u.set_password(passw)
		   u.save()
		   p = Profile.objects.create(user=u)
		   if request.FILES:
		      p.image = request.FILES['image']
		   p.save()
		   return HttpResponseRedirect(request.GET.get('next','/'))
		else:
		   form._errors["repeat"] = form.error_class(["Please enter password twice"])
		   form._errors["password"] = form.error_class(["Please enter password twice"])
	return render(request, 'signup.html', {	'poptags':poptags, 
						'popauthors':popauthors, 
						'form':form})

@login_required
def addquestion(request):
	poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
	form=AddQuestionForm()
	if request.user.is_authenticated():
	   if request.POST:
	      form = AddQuestionForm(request.POST)
	      if form.is_valid():
		 title = form.cleaned_data['title']
		 text = form.cleaned_data['text']
		 tags = form.cleaned_data['tags'].split(',')
		 author=request.user
		 q=Question.objects.create(author=author, title=title, text=text)
		 for t in tags:
		    if t.strip() != "":
		       try:
		         tag=Tag.objects.get(text=t.strip())
			 tag.rating+=1
			 tag.save()
		       except Tag.DoesNotExist:
			 tag=Tag.objects.create(text=t.strip())
		       q.tag_set.add(tag)
		 q.save()
		 return HttpResponseRedirect('/question?q='+str(q.id))
	else:
	   return HttpResponseRedirect('/signin')
	return render(request, 'addquestion.html', {'poptags':poptags, 
						    'popauthors':popauthors,
						    'form':form})

def settings(request):
	return HttpResponseRedirect('/')

def logout_v(request, page='/'):
	logout(request)
	return HttpResponseRedirect(page)

def getListFromPaginator(objlist, page, count):
	paginator=Paginator(objlist, count)
	objects=0
	try:
	   objects=paginator.page(page)
	except PageNotAnInteger:
	   objects=paginator.page(1)
	except EmptyPage:
	   raise Http404 #answers=paginator.page(paginator.num_pages)
	return objects

actions=frozenset({'new','pop','tag'})

def index(request):
	a=request.GET.get('a','new')
	tag=0
	if a not in actions:
	   raise Http404
	questions_list=0;
	if a=='new':
           questions_list = Question.objects.new()
	   title=u'Новые вопросы'
	if a=='pop':
	   questions_list =  Question.objects.popular()
	   title=u'Лучшие вопросы'
	if a=='tag':
	   tag=request.GET.get('tag','js')
	   title = u'Вопросы с тэгом "'+tag+'"'
	   questions_list = Question.objects.get_questions_by_tag(tag)
	page = request.GET.get('page',1)
	questions=getListFromPaginator(questions_list, page, 20)	
        poptags = get_popular_tags(10)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
        return render(request, 'index.html', {	'questions':questions, 
						'title':title, 
						'poptags':poptags, 
						'popauthors':popauthors,
						'a':a,
						'tag':tag})

def question(request):
	try:
	   q_id=long(request.GET.get('q'))
	except SyntaxError:
	   q_id=1
	except ValueError:
	   q_id=1
	except TypeError:
	   q_id=1
	try:
	   question = Question.objects.get(id=q_id)
	except ObjectDoesNotExist:
	   raise Http404
	answers_list=question.answer_set.all()
	tags = question.tag_set.all()
	poptags = get_popular_tags(10)
	page = request.GET.get('page', 1)
	answers=getListFromPaginator(answers_list, page, 20)
	popauthors=Profile.objects.get_queryset().order_by('-rating')[:authors]
	form=AnswerForm()
	if request.user.is_authenticated():
	   if request.POST:
		form = AnswerForm(request.POST)
		if form.is_valid():
		   text=form.cleaned_data['text']
		   author=request.user
		   answ=Answer.objects.create(text=text, question=question, author=author)
		   answ.save()
		   return HttpResponseRedirect('/question?q='+str(q_id))
	return render(request, 'question.html', {'question':question, 
						 'tags':tags, 
						 'poptags':poptags, 
						 'answers':answers, 
						 'popauthors':popauthors, 
						 'page':page,
						 'q':q_id,
						 'form': form })


'''
def params(request):
	if request.method=='POST':
	   req = request.POST
	else:
	   req = request.GET
	keys=req.keys()
	res='hello\n'
	for key in keys:
	   res+='\n'+key+'='+req[key]
	return render(request, 'params.html',{'params':res})'''
