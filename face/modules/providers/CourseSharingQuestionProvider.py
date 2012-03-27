import Provider as provider

from django.template.loader import get_template
from django.template import Context

import json, urllib2

####################################################################
########           CourseSharing Question Provider          ########
####################################################################
##
## This QuestionProvider is designed to plug directly into the 
## CourseSharing API.  The API uses CourseSharing both for 
## question retrieval and 


QUESTION_SERVER = 'http://localhost:7070/question_server_stub'

## Get all questions that are stored in the system.  This does
## not include any user permission filtering, which should be
## done outside of the data provider.
##
## Note: this method should always return a list of JSON objects.
def get_questions(user_id):
    def get_status(question):
        if question['answerable']:
            return 'released'
        elif question['gradable']:
            return 'gradable'
        return 'unknown'
    
    url = '%s/users/%s/questions' % (QUESTION_SERVER, str(user_id))
    f = urllib2.urlopen(url, None, 5000)
    third_party_questions = json.loads(f.read())

    question_tpl = get_template('question.tpl')
    questions = []
    
    for third_party_question in third_party_questions:
        question = {
            'status' : get_status(third_party_question),
            'question_id' : third_party_question['question_id'],
            'decoded_text' : third_party_question['content'],
            'time_released' : 'Today',
            'gradable' : third_party_question['gradable'],
            'answerable' : third_party_question['answerable'],
            'shared_with' : 'public',
        }
        question['html'] = question_tpl.render(Context({
            'question' : question
        }))
        questions.append(question) 

    return questions

## Get a single question as specified by the question_id.
##
## Note: this method should always return a single JSON object
## or raise an exception.
def get_question(question_id):
    questions = get_questions()
    
    for question in questions:
        if question['question_id'] == question_id:
            return question
    raise provider.ProviderException('A question with an ID of ' + question_id + ' does not exist.')

## Submits an attempt for the provided question.  Should return
## JSON object describing attempt.  This is also a good place to
## store the attempt if desired. 
##
## Response: {
##   correct : true / false
## }
def submit_attempt(question_id, user_id, attempt):
    raise NotImplementedError("submit_attempt() doesn't work for the CSQuestionProvider yet")
