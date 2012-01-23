from django.conf.urls.defaults import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'face.views.home', name='home'),
    # url(r'^face/', include('face.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ('^$', views.index),
    ('^authsub?token=([a-zA-Z0-9\%]+)$', views.authsub),
    ('account/create$', views.create_account),
    ('account/login$', views.login),
    ('account/logout$', views.logout),
    url('dash$', views.dash, name='dash'),
    ('question/check$', views.check_q),
    ('question/files/(\d+)', views.get_question_file),
    ('question/view/(\d+)', views.view_question),
    ('question/view/all$', views.list_questions),
    ('question/status/(\d+)', views.question_status),
    
    ('ajax/hints/basic/(\d+)', views.get_all_hints),
    ('ajax/hints/get/(\d+)/([a-z0-9]+)', views.get_hint_details),
    ('ajax/hints/submit/(\d+)', views.submit_hint),
    ('ajax/hints/vote/yes/([a-f0-9]+)', views.tally_vote, { 'vote' : True }),
    ('ajax/hints/vote/no/([a-f0-9]+)', views.tally_vote, { 'vote' : False }),
)
