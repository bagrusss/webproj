# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
import datetime

uploads = ""
default_photo="/user.png"

class Profile(models.Model):
   user=models.OneToOneField(User)
   rating=models.IntegerField(default=0)
   image = models.ImageField(upload_to = uploads, default = default_photo)
   def __unicode__(self):
	return str(self.rating)

class QuestionManager(models.Manager):
   def popular(self):
	return self.get_queryset().order_by('-rating')
   def new(self):
	return self.get_queryset().order_by('-created')
   def get_questions_by_tag(self, tag):	
	return self.get_queryset().filter(tag=Tag.objects.filter(text=tag))

class Question(models.Model):
   title = models.CharField(max_length=100) 
   text = models.TextField() 
   author = models.ForeignKey(User) 
   created = models.DateTimeField(default=datetime.datetime.now) 
   rating = models.IntegerField(default=0)
   def __unicode__(self):
       return self.title+" text: "+self.text
   objects = QuestionManager()

class Answer(models.Model):
   correct = models.BooleanField(default=0)
   text = models.TextField()
   author = models.ForeignKey(User)
   question = models.ForeignKey(Question)
   created = models.DateTimeField(default=datetime.datetime.now)
   rating = models.IntegerField(default=0)
   def __unicode__(self):
	return self.text
	
class TagManager(models.Manager):
    def popular(self):
	return self.get_queryset().order_by('-rating')
    def tags_for_questions(self, ques):
	return self.get_queryset().filter(question=ques)

class Tag(models.Model):
   rating = models.IntegerField(default=0)
   text = models.CharField(max_length=15) 
   #creator = models.ForeignKey(User)
   question = models.ManyToManyField(Question)
   objects = TagManager()
   def __unicode__(self):
	return self.text

class QuestionLike(models.Model):
   user=models.ForeignKey(User)
   question=models.ManyToManyField(Question)
   state=models.IntegerField(default=0) #0 - не лайкнут, 1 лайкнут, -1 дизлайкнут
   def __unicode__(self):
	return self.user +" q: "+self.question+" state: "+self.state

class AnswerLike(models.Model):
   user=models.ForeignKey(User)
   answer=models.ManyToManyField(Answer)
   state=models.IntegerField(default=0) #0 - не лайкнут, 1 лайкнут, -1 дизлайкнут
   def __unicode__(self):
	return self.user +" a: "+self.answer+" state: "+self.state
   
    
    
    
