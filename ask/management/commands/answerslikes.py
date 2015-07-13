# -*- coding: utf-8 -*-
from ask.management.commands.filldatabase import *

answer_first=[u"Попробуй", u"Посмотри", u"Глянь", u"Почитай", u"Возьми", u"Видел недавно", u"Поищи", u"Сгоняй"]

answer_second=[u"приклеить", u"порубить", u"зашить", u"форум", u"собрать", u"настроить", u"простроить", u"рассчитать", u"вырастить",
		u"с помощью", u"изобрел", u"здесь"]
answer_third=[u"документацию", u"литературу", u"озеро", u"топором", u"собрать", u"колесо", u"реле", u"raspberry pi", u"adruino",
		u"телефон", u"4dpa.ru"]

def gen_random_str():
    str1=answer_first[random.randint(0, len(answer_first)-1)]+" "+answer_second[random.randint(0, len(answer_second)-1)]
    str1+=" "+answer_third[random.randint(0, len(answer_third)-1)]+". "
    return str1


class Command(BaseCommand):
    
    def generete_answers(self):
	self.stdout.write("begin generate answers")
	u=User.objects.all()
	'''quest=Question.objects.get(id=1)
	txt_ping=u"Пинг"
	txt_pong=u"Понг"
	for i in range(1, 45):
	    if i%2==1:
		text=txt_ping
	    else:
		text=txt_pong
	    ans=Answer.objects.create(question=quest, author=u[random.randint(0, u.count()-1)],
					   text=text)
	    ans.save()	'''	
	q=Question.objects.all()
	for i in range (1, answer_count):
	    text=gen_random_str()
	    text+=gen_random_str()
	    answ=Answer.objects.create(text=text, author=u[random.randint(0, u.count()-1)],
					question=q[random.randint(0, q.count()-1)])
	    answ.save()
	    if i%50 == 0:
		self.stdout.write("generated %s answers" %i)
	self.stdout.write("finish generate answers")
	return

    def set_tag_rating0():
	self.stdout.write("begin set tag rating")
	tags=Tag.objects.all()
	for t in tags:
	   t.rating=0;
	   t.save()
	self.stdout.write("finish set tag rating")
	return


    def handle(self, *args, **options):
	self.stdout.write("begin manage command")
	self.generete_answers()
	#self.set_tag_rating0()
	self.stdout.write("finish manage command")
	return






