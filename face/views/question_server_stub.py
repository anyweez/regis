from django.http import HttpResponse

import json

import urllib2 # for Django requests to third party servers 
import json, datetime
import face.util.UserStats as UserStats
import face.models.models as models
import face.msg.msghub as msghub
import face.util.exceptions as exception
import face.util.QuestionManager as qm




def questions(request):
    if 'POST' == request.method or \
            ('POST' in request.REQUEST and request.REQUEST['POST'] == 'DEBUG'):
        question = {
            'kind' : 'freeresponsequestion',
            'question_id' : 3,
            'content' : 'Question content from third party server', 
            'answerable' : True,
            'gradable' : False,
            'author' : 'User id goes here',  
            'answers' : ['Answer 1', 'Answer 2'], 
            'rubricsuggestions' : [
                'Included answer 1', 
                'Missed the point of the question'
            ], 
            'max_score' : 5, 
            'shared_with' : 'public',
        }
        return HttpResponse(json.dumps(question), mimetype='application/json')
    if 'GET' == request.method:
        questions = []
        for x in xrange(10):
            questions.append( {
                "question_id" : x,
                "kind" : "question",
                "content" : "Content and text for question%d" % x,
                "answerable" : True,
                "gradable" : False,
            } )
        return HttpResponse(json.dumps(questions), mimetype='application/json')



