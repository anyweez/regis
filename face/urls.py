from django.conf.urls.defaults import patterns, include, url
import views.main as main
import views.admin as admin

urlpatterns = patterns('',
    ('^$', main.index),
    ('^login$', main.index),
    ('^about$', main.about),
#    ('account/create$', main.create_account),
    ('account/logout$', main.logout),
    
    ('admin', admin.index),
    
    ('^build-acct$', main.build_acct),
    ('dash$', main.dash),
    ('^how$', main.howitworks),
    ('question/check$', main.check_q),
    ('question/files/(\d+)', main.get_question_file),
    ('question/view/(\d+)', main.view_question),
    ('question/view/all$', main.list_questions),
    ('question/status/(\d+)', main.question_status),
    ('suggest$', main.suggest_q),
    ('suggest/submit$', main.submit_suggestion),
    ('ajax/feedback/like/(\d+)/(\d+)', main.feedback_like),
    ('ajax/feedback/challenge/(\d+)/(\d+)', main.feedback_challenge),
    ('ajax/hints/basic/(\d+)', main.get_all_hints),
    ('ajax/hints/get/(\d+)/([a-z0-9]+)', main.get_hint_details),
    ('ajax/hints/submit/(\d+)', main.submit_hint),
    ('ajax/hints/vote/yes/([a-f0-9]+)', main.tally_vote, { 'vote' : True }),
    ('ajax/hints/vote/no/([a-f0-9]+)', main.tally_vote, { 'vote' : False }),
    ('^questions/list$', main.list_questions_with_api),
    ('^questions/(\d+)$', main.view_question_with_api),
    ('^questions', main.questions_unknown), # Redirect to /questions/list
    ('^api/questions/list$', main.api_questions_list),
    ('^api/questions/([0-9]+)$', main.api_questions_get),
    ('^api/hints/list/([0-9]+)$', main.api_hints_list),
    ('^api/hints/([0-9]+)/vote$', main.api_hints_vote),
    ('^api/hints/([0-9]+)$', main.api_hints_get),
    ('^api/attempts/insert/([0-9]+)$', main.api_attempts_insert),
    ('^api/attempts/([0-9]+)$', main.api_attempts_get),
    ('^api/attempts/list/([0-9]+)$', main.api_attempts_list),
    ('^system/tests/run$', main.system_tests_run),
    url(r'', include('social_auth.urls')),
)
