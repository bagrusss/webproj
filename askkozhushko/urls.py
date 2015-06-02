from django.conf.urls import patterns, include, url
from django.contrib import admin
from ask.views import index, signup, signin, question, addquestion, params
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),
    url(r'^params$', 'ask.views.params', name='params'),
    url(r'^$', 'ask.views.index', name='index'),
    url(r'^signup$', 'ask.views.signup', name='signup'),
    url(r'^signin$', 'ask.views.signin', name='signin'),
    url(r'^question$', 'ask.views.question', name='question'),
    url(r'^addquestion$', 'ask.views.addquestion', name='addquestion'),
    #url(r'^admin/', include(admin.site.urls)),
)
