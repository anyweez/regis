from django.conf.urls.defaults import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    ('^$', views.index),
    ('^login$', views.index),
    ('^about$', views.about),
#    ('account/create$', views.create_account),
    ('account/logout$', views.logout),
    ('^build-acct$', views.build_acct),
    ('dash$', views.dash),
    ('^how$', views.howitworks),
    ('question/check$', views.check_q),
    ('question/files/(\d+)', views.get_question_file),
    ('question/view/(\d+)', views.view_question),
    ('question/view/all$', views.list_questions),
    ('question/status/(\d+)', views.question_status),
    ('suggest$', views.suggest_q),
    ('suggest/submit$', views.submit_suggestion),
    ('ajax/feedback/like/(\d+)/(\d+)', views.feedback_like),
    ('ajax/feedback/challenge/(\d+)/(\d+)', views.feedback_challenge),
    ('ajax/hints/basic/(\d+)', views.get_all_hints),
    ('ajax/hints/get/(\d+)/([a-z0-9]+)', views.get_hint_details),
    ('ajax/hints/submit/(\d+)', views.submit_hint),
    ('ajax/hints/vote/yes/([a-f0-9]+)', views.tally_vote, { 'vote' : True }),
    ('ajax/hints/vote/no/([a-f0-9]+)', views.tally_vote, { 'vote' : False }),
    ('^questions/list$', views.list_questions_with_api),
    ('^questions/(\d+)$', views.view_question_with_api),
    ('^questions', views.questions_unknown), # Redirect to /questions/list
    ('^api/questions/list$', views.api_questions_list),
    ('^api/questions/([0-9]+)$', views.api_questions_get),
    ('^api/hints/list/([0-9]+)$', views.api_hints_list),
    ('^api/hints/([0-9]+)/vote$', views.api_hints_vote),
    ('^api/hints/([0-9]+)$', views.api_hints_get),
    ('^api/attempts/insert/([0-9]+)$', views.api_attempts_insert),
    ('^api/attempts/([0-9]+)$', views.api_attempts_get),
    ('^api/attempts/list/([0-9]+)$', views.api_attempts_list),
    ('^system/tests/run$', views.system_tests_run),
    url(r'', include('social_auth.urls')),
)
