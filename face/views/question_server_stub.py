from django.http import HttpResponse

import json

def questions(request, user):
    questions = []
    for x in xrange(10):
        questions.append( {
            "id" : x,
            "kind" : "question",
            "content" : "Content and text for question%d" % x,
            "answerable" : True,
            "gradable" : False,
        } )
    return HttpResponse(json.dumps(questions), mimetype='application/json')



