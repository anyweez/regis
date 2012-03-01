from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import strip_tags

import face.models.models as users
import face.util.UserStats as UserStats
import face.util.QuestionManager as qm
import face.util.Concierge as question_link
import face.msg.msghub as msghub
import face.util.exceptions as exception

import re, json, math, datetime

@login_required
def api_questions_list(request):
    qs = users.QuestionSet.objects.get(reserved_by=request.user)
    all_questions = qs.questions.all().order_by('template')
    items = []
    options = { 'html' : 'thumbnail' }
    for question in all_questions:
        if question.status in ['released', 'ready', 'solved']:
            items.append(questions_get_json(request, question.template.id, question=question, options=options))
    response = { "kind" : "questionFeed",
		"items" : items }
    return HttpResponse(json.dumps(response), mimetype='application/json')

@login_required
def api_questions_get(request, question_id):
    return HttpResponse(json.dumps(questions_get_json(request, question_id)),
                        mimetype='application/json')

'''
questions_get_json is used by the API call get and list.
This function handles all permissions and formats the JSON
response with the appropriate fields.
If the question does not exist, return a "question#notfound" package.
If the question is "locked", return some fields.
If the questions is "released", return everything.
By default, send the HTML snippet in the 'html' attribute
for embedding in a web page. 
Options can be passed in, like { 'html' : 'thumbnail' } which
requests only the small view to be embeded in list form.
'''
def questions_get_json(request, question_id, question=None, options=None):
    user = request.user
    errors = []
    hintids = []
    def create_not_found_package():
        response = { "kind" : "question#notfound" }
        if options['html'] == 'full':
            response['html'] = render_to_response('include/questions_get.tpl',
                                { 'questionstatus' : "doesnotexist",
                                  'questiontitle' : "Question not found",
                                  'questionnumber' : question_id,
                                  'questioncontent' : "This question does not exist. Contact us if you think this is a mistake.",
                                  'questionpublished' : "",
                                  'hintsids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'thumbnail':
            response['html'] = render_to_response('include/questions_get_thumbnail.tpl',
                                { 'questionstatus' : "doesnotexist",
                                  'questiontitle' : "Question not found",
                                  'questionnumber' : question_id,
                                  'questioncontent' : "This question does not exist. Contact us if you think this is a mistake.",
                                  'questionpublished' : "",
                                  'hintids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        else:
            pass
        return response
            
    def create_locked_package(question, options):
        response = { "kind" : "question",
                     "status" : question.status,
                     "key" : question.id,
		     "title" : question.template.title,
                     "id" : question.template.id,
                     "errors" : errors }
        if options['html'] == 'full':
            response['html'] = render_to_response('include/questions_get.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : "Oops, this questions is locked. Keep working and you'll be here soon!",
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'thumbnail':
            response['html'] = render_to_response('include/questions_get_thumbnail.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : "Oops, this questions is locked. Keep working and you'll be here soon!",
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        else:
            pass
        return response
    def create_question_package(question, options):
        response = { "kind" : "question",
                     "status" : question.status,
                     "key" : question.id,
		     "title" : question.template.title,
                     "id" : question.template.id,
  		     "content" : question.decoded_text(),
  		     #"scope" : scope,
  		     "hints" : hintids, 
  		     "url" : "http://%s/questions/%d" % (request.get_host(), question.template.id),
  		     "published" : str(question.time_released),
  		     "actor" : question.user.id,
                     "errors" : errors }
        if options['html'] == 'thumbnail':
            response['html'] = render_to_response('include/questions_get_thumbnail.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : question.decoded_text(),
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : hintids },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'full':
            response['html'] = render_to_response('include/questions_get.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : question.decoded_text(),
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : hintids },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'hide':
            if 'html' in response:
                del response['html']
        else:  
            if 'html' in response:
                del response['html']
        return response
    # Figure out options
    # html=full [default] or html=thumbnail or html=hide
    html_options = ['full', 'thumbnail', 'hide']
    if options is None:
        options = {}
    if 'html' in options \
       and options['html'] in html_options:
        pass
    elif 'html' in request.GET \
         and request.GET['html'] in html_options:
        options['html'] = request.GET['html']
    else:
        options['html'] = 'full'
    if question is None:
        # First try to find the question.
        # If the question does not exist, return a does not exist package.
        try:
            template = users.QuestionTemplate.objects.get(id=question_id)
            if template is not None:
                question = users.Question.objects.filter(user=user, template=template)
                if len(question) > 0:
                    if len(question) > 1:
                        errors.append("Redundant questions found.")
                    question = question[0]
                else:
                    return create_not_found_package()
            else:
                return create_not_found_package()
        except users.QuestionTemplate.DoesNotExist as error:
            return create_not_found_package()
        except users.Question.DoesNotExist as error:
            return create_not_found_package()
    # Get all hints
    try:
        hints = users.QuestionHint.objects.filter(template=question.template.id)
        if hints is not None:
            hintids = [h.id for h in hints]
    except users.QuestionHint.DoesNotExist as error:
        errors.append("Error when looking for hints")
    # If pending or ready, return a locked package.
    if question.status in ['pending', 'ready']:
        return create_locked_package(question, options)
    # This must be a released questions
    elif question.status in ['released', 'solved']:
        return create_question_package(question, options)
    errors.append("Question status unknown")
    return create_question_package(question, options)

@login_required
def api_hints_list(request, question_id):
    def create_not_found_package():
        return { "kind" : "hint#notfound" }
    try:
        hints = users.QuestionHint.objects.filter(template__id=question_id)
        items = []
        options = { "fields" : "kind,id" }
        for hint in hints:
            items.append(hints_get_json(request, hint.id, hint=hint, options=options))
        response = { "kind" : "hintFeed",
                     "question" : question_id,
                     "items" : items }
        return HttpResponse(json.dumps(response),
                            mimetype='application/json')
    except users.QuestionHint.DoesNotExist as error:
        return HttpResponse(json.dumps(create_not_found_package()),
                            mimetype='application/json')

@login_required
def api_hints_vote(request, hint_id):
    if request.method != 'POST':
        return HttpResponse(json.dumps({ "kind" : "Expecting POST request" }),
                            mimetype='application/json')
    hint_id = int(request.POST['id'])
    rating = request.POST['rating']
    if rating == 'yes':
        rating = True
    elif rating == 'no':
        rating = False
    else:
        return HttpResponse(json.dumps({ "kind" : "Bad hint vote", 
                                   }),
                            mimetype='application/json')
 
    hint = users.QuestionHint.objects.get(id=hint_id)
    if hint is None:
        return HttpResponse(json.dumps({ "kind" : "hint#notfound", 
                                   }),
                            mimetype='application/json')
    

    # Check to make sure that the user hasn't voted 
    prev_ratings = users.QuestionHintRating.objects.filter(hint=hint, src=request.user)
    if len(prev_ratings) > 0:
        approval = prev_ratings[0].rating
        response = { "kind" : "message" }
        if approval:
            response['message'] = "You've already upvoted this hint."
        else:
            response['message'] = "You've already downvoted this hint."
    else:
        users.QuestionHintRating(hint=hint, src=request.user, rating=rating).save()
        response = hints_get_json(request, hint_id, hint=hint)
    
    return HttpResponse(json.dumps(response), mimetype='application/json')

@login_required
def api_hints_get(request, hint_id):
    return HttpResponse(json.dumps(hints_get_json(request, hint_id)),
                        mimetype='application/json')

def hints_get_json(request, hint_id, hint=None, options=None):
    def create_not_found_package():
        return { "kind" : "hint#notfound" }
    if hint is None:
        try:
            hint = users.QuestionHint.objects.get(id=hint_id)
            if hint is None:
                return create_not_found_package()
        except users.QuestionHint.DoesNotExist as error:
            return create_not_found_package() 
    # Get rating
    hintsup = users.QuestionHintRating.objects.filter(hint=hint, rating=True)
    hintsdown = users.QuestionHintRating.objects.filter(hint=hint, rating=False)
    votetotal = len(hintsup) - len(hintsdown)
    response = { "kind" : "hint",
                 "id" : hint.id,
                 "content" : hint.text,
                 "question" : hint.template.id,
                 "rating" : votetotal,
                 "actor" : hint.src.id } 
    # Add HTML
    response['html'] = render_to_response('include/hints_get.tpl',
                      { 'hintid' : hint.id,
                        'hintcontent' : hint.text,
                        'votetotal' : votetotal },
                      context_instance=RequestContext(request)
                      ).content
    # Handle masking of certain fields based on the fields parameter
    parameters = ['fields']
    if options is None:
        options = {}
    for p in parameters:
        if p in request.GET and p not in options:
            options[p] = request.GET[p]
    if 'fields' in options:
        fields = options['fields'].split(',')
        for k in response.keys():
            if k not in fields:
                del response[k]
    return response


#Example: 'api/attempts/insert', views.api_attempts_insert
@login_required
def api_attempts_insert(request, question_id):
    errors = []
    question_id = int(question_id)
    if request.method != 'POST':
        return HttpResponse(json.dumps({ "kind" : "Expecting POST request" }),
                            mimetype='application/json')
    if 'content' in request.POST:
        content = request.POST['content']
        if len(content) == 0:
            errors.append("Length of content is 0")
    else:
        errors.append("No content given")
    
    if len(errors) > 0:
        return HttpResponse(json.dumps({ "kind" : "error", 
                                         "errors" : errors,
                                   }),
                            mimetype='application/json')
    try: 
        question = users.Question.objects.get(template__id=question_id, user=request.user)
    except users.Question.DoesNotExist:
        raise exception.UnauthorizedAttemptException(request.user, question_id)
    if question is None:
        return HttpResponse(json.dumps({ "kind" : "question#notfound", 
                                   }),
                            mimetype='application/json')
    if question.status != 'released':
        errors.append('Cannot attempt question with status "%s"' % question.status)
    if len(errors) > 0:
        return HttpResponse(json.dumps({ "kind" : "error", 
                                         "errors" : errors,
                                   }),
                            mimetype='application/json')
         
    question_m = qm.QuestionManager()
    correct, msg = question_m.check_question(question, content)
    
    msghub.register_message(msg, target=question_id, status=correct)
    
    # Record the guess.
    g = users.Guess(user=request.user, 
                    question=question, 
                    value=content, 
                    correct=correct, 
                    time_guessed=datetime.datetime.now())
    g.save()
    if correct and question.status != 'solved':
        question.status = 'solved'
        question.save()
        try:
            question_m = qm.QuestionManager()
            # Activate the next question.
            question_m.activate_next(request.user)
        except exception.NoQuestionReadyException:
            # TODO cartland: Should we record this?
            pass
    response = attempts_get_json(request, attempt_id=g.id, attempt=g)
    return HttpResponse(json.dumps(response), mimetype='application/json')

@login_required
def api_attempts_list(request, question_id):
    question_id = int(question_id)
    def create_not_found_package():
        return { "kind" : "attempt#notfound" }
    try:
        attempts = users.Guess.objects.filter(question__template__id=question_id)
        items = []
        options = { "fields" : "kind,id,content,correct,html",
                    "html" : "thumbnail" }
        for attempt in attempts:
            items.append(attempts_get_json(request, attempt.id, attempt=attempt, options=options))
        response = { "kind" : "attemptFeed",
                     "question" : question_id,
                     "items" : items }
        return HttpResponse(json.dumps(response),
                            mimetype='application/json')
    except users.QuestionHint.DoesNotExist as error:
        return HttpResponse(json.dumps(create_not_found_package()),
                            mimetype='application/json')

def api_attempts_get(request, attempt_id):
    return HttpResponse(json.dumps(attempts_get_json(request, attempt_id)),
                        mimetype='application/json')

def attempts_get_json(request, attempt_id, attempt=None, options=None):
    def create_not_found_package():
        return { "kind" : "attempt#notfound" }
    def get_attempt_html(attempt):
        return "%s, '%s', %s" % (str(attempt.time_guessed), attempt.value, "Correct" if attempt.correct else "Incorrect")
    if attempt is None:
        try:
            attempt = users.Guess.objects.get(id=attempt_id)
            if attempt is None:
                return create_not_found_package()
        except users.Guess.DoesNotExist as error:
            return create_not_found_package() 
    response = { "kind" : "attempt",
                 "id" : attempt.id,
                 "content" : attempt.value,
#                 "attempt_index" : attempt.index,
                 "html" : get_attempt_html(attempt),
                 "question" : attempt.question.template.id,
                 "correct" : attempt.correct,
  		 "url" : "http://%s/questions/%d" % (request.get_host(), attempt.question.template.id),
                 "published" : str(attempt.time_guessed),
                 "actor" : attempt.user.id } 
    # Handle masking of certain fields based on the fields parameter
    parameters = ['fields']
    if options is None:
        options = {}
    for p in parameters:
        if p in request.GET and p not in options:
            options[p] = request.GET[p]
    if 'fields' in options:
        fields = options['fields'].split(',')
        for k in response.keys():
            if k not in fields:
                del response[k]
    return response


@login_required
def api_community_questions_list(request):
    templates = users.QuestionTemplate.objects.filter(community=True)
    items = []
    options = { 'html' : 'thumbnail' }
    for template in templates:
        question = get_community_question_from_template(template)
        items.append(community_questions_get_json(request, template.id, question=question, options=options))
    response = { "kind" : "communityFeed",
		 "items" : items }
    return HttpResponse(json.dumps(response), mimetype='application/json')


@login_required
def api_community_questions_get(request, question_id):
    return HttpResponse(json.dumps(community_questions_get_json(request, question_id)),
                        mimetype='application/json')
  
@login_required
def api_community_questions_insert(request):
    errors = []
    messages = []
    if request.method != 'POST':
        errors.append("Expecting POST request for adding questions.")
        messages.append("Expecting POST request for adding questions.")
        return HttpResponse(json.dumps({ "kind" : "error",
                                         'errors' : errors,
                                         'messages' : messages,
                                       }),
                            mimetype='application/json')
    question = None
    answer = None
    subjective = None
    if 'question' in request.POST:
        question_id = request.POST['question']
    else:
        errors.append("No question given")
        messages.append("No question given")
    if 'answer' in request.POST:
        answer = request.POST['answer']
    else:
        subjective = True
    if subjective is not None:
        if subjective != True:
            errors.append("Server problem configuring question data")
        else:
            pass # Subjective is True
    elif 'subjective' in request.POST:
        subjective = request.POST['subjective']
        if subjective == 'free':
            subjective = True
        elif subjective == 'exact':
            subjective = False
        else:
            error = "Unknown community question 'subjective': %s" % subjective
            errors.append(error)
            messages.append(error)
    else:
        error = "Missing field 'subjective' in order to create a question"
        errors.append(error)
        messages.append(error)
    
    if len(errors) > 0:
        return HttpResponse(json.dumps({ "kind" : "error", 
					 "messages" : message,
                                         "errors" : errors,
                                   }),
                            mimetype='application/json')
    
    # question, answer, and subjective are guarnateeed to exist.
    # TODO update the TemplateModel to store an Answer
    users.QuestionTemplate(text=question, answer=answer, subjective=subjective, community=True)
    if len(errors) > 0:
        return HttpResponse(json.dumps({ "kind" : "error", 
                                         "errors" : errors,
                                   }),
                            mimetype='application/json')
         
    question_m = qm.QuestionManager()
    correct, msg = question_m.check_question(question, content)
    
    msghub.register_message(msg, target=question_id, status=correct)
    
    # Record the guess.
    g = users.Guess(user=request.user, 
                    question=question, 
                    value=content, 
                    correct=correct, 
                    time_guessed=datetime.datetime.now())
    g.save()
    if correct and question.status != 'solved':
        question.status = 'solved'
        question.save()
        try:
            question_m = qm.QuestionManager()
            # Activate the next question.
            question_m.activate_next(request.user)
        except exception.NoQuestionReadyException:
            # TODO cartland: Should we record this?
            pass
    response = attempts_get_json(request, attempt_id=g.id, attempt=g)
    return HttpResponse(json.dumps(response), mimetype='application/json')
    
    question_id = 2000
    return HttpResponse(json.dumps(community_questions_get_json(request, question_id)),
                        mimetype='application/json')


def community_questions_get_json(request, question_id, options=None):
    errors = ['This is stub code']
    # Figure out options
    # html=full [default] or html=thumbnail or html=hide
    html_options = ['full', 'thumbnail', 'hide']
    if options is None:
        options = {}
    if 'html' in options \
       and options['html'] in html_options:
        pass
    elif 'html' in request.GET \
         and request.GET['html'] in html_options:
        options['html'] = request.GET['html']
    else:
        options['html'] = 'full'

    response = { "kind" : "communityQuestion",
                 "id" : question_id,
                 "status" : "released",
                 "content" : "What is recursion?",
                 "title" : None,
                 "published" : "Yesterday",
                 "solver_name" : None, 
                 "errors" : errors }
    if options['html'] == 'thumbnail':
        response['html'] = render_to_response('include/questions_get_thumbnail.tpl',
           { 'questionstatus' : response['status'],
             'questiontitle' : response['title'],
             'questionnumber' : response['id'],
             'questioncontent' : response['content'],
             'questionpublished' : response['published'],
           },
           context_instance=RequestContext(request)
           ).content
    elif options['html'] == 'full':
        response['html'] = render_to_response('include/questions_get.tpl',
           { 'questionstatus' : response['status'],
             'questiontitle' : response['title'],
             'questionnumber' : response['id'],
             'questioncontent' : response['content'],
             'questionpublished' : response['published'],
           },
           context_instance=RequestContext(request)
           ).content
    else:
        pass
    return response
