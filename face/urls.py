from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
import views.core as core
import views.admin as summary
import views.api as api
import views.question_server_stub as question_server_stub

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
    ('^api/decks/users$', api.get_users),
#    ('^api/decks/([a-f0-9]+)', api.get_deck),
    
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
    ('^questions', core.questions_unknown), # Redirect to /questions/list
    ('^api/questions$', api.api_questions),
    ('^api/decks$', api.api_decks),
    ('^api/decks/(\d+)$', api.api_deck),
    ('^question_server_stub/questions$', question_server_stub.questions),
    ('^api/questions/fakelist$', api.fakelist),
    
    ('^test/thirdpartylatency$', api.test_third_party_latency),
    ('^test/latency$', core.test_latency),
    ('^system/tests/run$', core.system_tests_run),
    ('^sanity/questions/([0-9]+)$', core.sanity_questions_get),
    url(r'', include('social_auth.urls')),
)
