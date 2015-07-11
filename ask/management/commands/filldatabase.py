# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from ask.models import *
import random, string
from django.db import IntegrityError

def prepare_images():
   imgs=[]
   for i in range(1, 9):
	imgs.append("img"+str(i)+".jpg")
   return imgs
images=prepare_images()
first_names=[	"John", "David", "Alex", "Vladimir", "Victor", "Vasily", "Alexey", "Petr", "Semen", "Anna", 
		"Maria", "Susana", "Oleg", "Olga", "Boris", "Ivan", "Mark", "Nadejda", "Gregor", "Andrey", 
		"Bran", "Roman", "Romor", "Poul", "Alla", "Maxim", "Anastasia", "Rita", "Irina",  
		"Sherlok", "Michael", "Lisbet", "Martin", "Henry", "Fedor", "Sergey", "Arnold", "Van", "Dmitry",
		"Svyatoslav", "Vyacheslav", u"Ярополк", u"Дарья", u"Алена", u"Полина", u"Василиса", u"Жанна", u"Регина", u"Маша", 
		u"Ольга", u"Кристина", u"Валерия", u"Екатерина", u"Юлия", u"Юрий", u"Юлий", u"Виталий", u"Алена", u"Прохор",
		u"Ванесса", u"Инесса",   u"Евгений", u"Евгения", u"Марина", u"Денис", u"Богдан", u"Валентин", u"Валентина",
		u"Леонид", u"Степан", u"Георгий", u"Виктор", u"Алена",  u"Оксана", u"Владимир", u"Милена", u"Остап", u"Антон",
		u"Ян", u"Федот", u"Сильвестр", u"Брюс", u"Жан-Клодт", u"Любава", "Robert", "Daniel", "Bred", "Ross", 
		"Ruso", "Varis", "Wayne", "James", "Richard", "Jeremi", "Tomas", "Daniel", "Milla", "Dog"   ]

second_names=[	"Bolton", "Stark", "Tyrell", "Smith", "Colt", "Brown", "White", "Blask", "Dick", "Pete", 
		"Whillis", "Van-Damm", "Putin", "Asirov", "Patrick", "Binn", "Cruse", "Yolovich", "Gregor", "Bushemi", 
		"Aristov", "Romanov", "Besverhny", "Suzev", "Andropov", "Borman", "April", "Blon", "Irdy",  
		"Sherlok", "Michael", "Lisbet", "Martin", "Henry", "Fedor", "Sergey", "Arnold", "Van", "Dmitry",
		"Svyatoslav", "Vyacheslav", u"Семенов", u"Иванов", u"Романов", u"Поликарпов", u"Панин", u"Голов", u"Тодоренко", u"Мартова", 
		u"Васильева", u"Андреев", u"Харламова", u"Мухин", u"Токарев", u"Григорьев", u"Захарьев", u"Портунов", u"Коршунов", u"Молотов",
		u"Станин", u"Хромов",   u"Храмов", u"Чернов", u"Бортов", u"Болотов", u"Болтон", u"Валентин", u"Валентина",
		u"Леонид", u"Степан", u"Георгий", u"Янк", u"Алена",  u"Оксана", u"Владимир", u"Милена", u"Остап", u"Антон",
		u"Ян", u"Федот", u"Сильвестр", u"Брюс", u"Жан-Клодт", u"Любава", "Robert", "Daniel", "Bred", "Ross", 
		"Ruso", "Varis", "Wayne", "James", "Richard", "Jeremi", "Tomas", "Daniel", "Cat", "Dog"    ]

question_first=[u"Почему", u"Как", u"Когда", u"Кто", u"Сколько", u"Каким образом", u"Где", u"Зачем"]

question_second=[u"проходит", u"регулировать", u"пропал", u"случилось", u"собрать", u"настроить", u"простроить", u"рассчитать", u"вырастить",
		u"разобрать", u"изобрел", u"прошить"]
question_third=[u"лом", u"лунопарк", u"тормоза", u"нашествие", u"собрать", u"колесо", u"концерт", u"певец", u"дерево",
		u"телефон", u"лампочку"]
question_quard=[u"в России", u"с помощью отвертки", u"без наличия опыта", u"своими руками", u"дешево и сердито", 
		u"с минимальными потерями", u"из-за границы", u"под Linux", u"в америкосии", u"в гараже", u"на озере"]
	
user_count=10000;
question_count=100000;
tags_count=10000;
answer_count=1000000
def randomtext(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

class Command(BaseCommand):    
    
    def generate_tags(self):
	self.stdout.write("begin generate tags")
	for i in range(1, tags_count):
		tag=Tag.objects.create(text=randomtext(random.randint(7,15)), rating=random.randint(0,250))
		tag.save()
	self.stdout.write("finish generate tags")
	return
    def generate_users(self):
	self.stdout.write("begin generate users")
	for i in range(1, user_count):
	  	fname=first_names[random.randint(0, len(first_names)-1)]
	   	sname=second_names[random.randint(0, len(second_names)-1)]
		uname=fname+"_"+sname[0]+str(i)
		u=User.objects.create_user(username=uname, first_name=fname, last_name=sname)
		try:
		   u.set_password(randomtext(15))
		   u.save()
		   p=Profile.objects.create(user=u, rating=random.randint(0, 999), image=images[random.randint(0, len(images)-1)])
		   p.save()
		except IntegrityError:
		   i-=1
		if i%10 == 0:
		   self.stdout.write("generated "+str(i)+" users")
	self.stdout.write("finish generate users")
	return

    def generate_question(self):
	u=User.objects.all()
	tags=Tag.objects.all()
	self.stdout.write("begin generate questions")
	for i in range(1, question_count):
	   title=question_first[random.randint(0, len(question_first)-1)]+" "+question_second[random.randint(0, len(question_second)-1)]
	   text=title+" "+question_third[random.randint(0, len(question_third)-1)]+" "+question_quard[random.randint(0, len(question_quard)-1)]+"?"
	   auth=u[random.randint(0, user_count)]
	   q=Question.objects.create(title=title, text=text, author=auth)
	   for k in range(0, random.randint(1, 3)):
		q.tag_set.add(tags[random.randint(1, tags.count()-1)])
	   q.save()
	   if i%10==0:
	        self.stdout.write("%s questions generated" %i)
	self.stdout.write("finish generate questions")

    def handle(self, *args, **options):
	self.stdout.write("start manage command")
	self.generate_tags()
	self.generate_users()
	self.generate_question()
	self.stdout.write("finish manage command")
	return 0








