from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
import views.core as core
import views.admin as summary
import views.api as api

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^robots\.txt$', direct_to_template, {'template': 'robots.tpl', 'mimetype': 'text/plain'}),
    ('^$', core.index),
    ('^path$', core.path),
    
    ('^api/decks/home$', api.home_deck),
    ('^api/decks/([a-f0-9]+)', api.get_deck),
    
    
    
    ('^login$', core.index),
    ('^about$', core.about),
    ('^bomb$', core.bomb),
    ('account/logout$', core.logout),
    ('^build-acct$', core.build_acct),
    ('dash$', core.dash),
    ('^how$', core.howitworks),
    ('question/check$', core.check_q),
    ('question/files/(\d+)', core.get_question_file),
#    ('question/view/(\d+)', core.view_question),
    ('question/view/all$', core.list_questions),
    ('question/status/(\d+)', core.question_status),
    ('suggest$', core.suggest_q),
    ('suggest/submit$', core.submit_suggestion),
    ('ajax/feedback/like/(\d+)/(\d+)', core.feedback_like),
    ('ajax/feedback/challenge/(\d+)/(\d+)', core.feedback_challenge),
    ('ajax/hints/basic/(\d+)', core.get_all_hints),
    ('ajax/hints/get/(\d+)/([a-z0-9]+)', core.get_hint_details),
    ('ajax/hints/submit/(\d+)', core.submit_hint),
    ('ajax/hints/vote/yes/([a-f0-9]+)', core.tally_vote, { 'vote' : True }),
    ('ajax/hints/vote/no/([a-f0-9]+)', core.tally_vote, { 'vote' : False }),
    ('^questions/list$', api.list_questions_with_api),
    ('^questions/(\d+)$', api.view_question_with_api),
    ('^questions', core.questions_unknown), # Redirect to /questions/list
    ('^api/questions/list$', api.api_questions_list),
    ('^api/questions/([0-9]+)$', api.api_questions_get),
    ('^api/hints/list/([0-9]+)$', api.api_hints_list),
    ('^api/hints/([0-9]+)/vote$', api.api_hints_vote),
    ('^api/hints/([0-9]+)$', api.api_hints_get),
    ('^api/questions/([0-9]+)/attempts/insert$', api.api_attempts_insert),
    ('^api/attempts/([0-9]+)$', api.api_attempts_get),
    ('^api/questions/([0-9]+)/attempts/list$', api.api_attempts_list),
    ('^api/questions/fakelist$', api.fakelist),
    
    ('^system/tests/run$', core.system_tests_run),
    ('^sanity/questions/([0-9]+)$', core.sanity_questions_get),
    url(r'', include('social_auth.urls')),
)
