from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import face.models.models as models
import face.util.QuestionManager as qm
import face.util.FileManager as fm
import face.util.exceptions as exception
import face.modules.providers.Provider as provider

import json

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
    return render_to_response('index.tpl',
        context_instance=RequestContext(request))

@login_required
def path(request):
    return render_to_response('path.tpl')

# This is the major login method.  After the social-auth module
# has processed the user's login, we do a couple of things.
#
# 1) If this is the user's first login, do some important acct
#    info generation.  Change their username, assign them to
#    a question set, and generate a RegisUser record for them.
# 2) For all users, check to see if a new question needs to be
#    released.
# 3) Record that the user is logging in.
# 4) Forward them to the dashboard ("/dash").
@login_required
def build_acct(request):
    ruser = None
    try:
        ruser = models.RegisUser.objects.get(user=request.user)
    except models.RegisUser.DoesNotExist:
        # Update the user's username.
        u = request.user
        u.username = '%s %s' % (u.first_name, u.last_name)
        # TODO: We should let them change their name at some point as well...
        u.save()

        # Create their RegisUser record
        # TODO: id=1 shouldn't be hard-coded here.      
        league = models.RegisLeague.objects.get(id=1)
        ruser = models.RegisUser(user=u, league=league)
        ruser.save()
        
    question_m = qm.QuestionManager()
    question_m.bind_questions(request.user)
        
    # Save an event recording that the user just logged in. 
    models.RegisEvent(who=request.user, event_type="login").save()
                
    # If the user hasn't had a question released in 48 hours, release
    # a new one.
    try:
        # Check to see whether the user needs a new question and release
        # if so.  If there isn't one ready, don't do anything (since there's
        # nothing we can really do).
        question_m.activate_next(request.user)
    except exception.NoQuestionReadyException:
        pass

    # Correct, let's proceed.
    return redirect('/path')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required
def get_question_file(request, tid):
    # Get the template so that we can run a query for the QuestionInstance.
    try:
        template = models.QuestionTemplate.objects.get(id=tid)
    except models.QuestionTemplate.DoesNotExist:
        return render_to_response('error.tpl', 
            { 'errors' : ["The template you requested isn't valid."] })
    
    # Get the QuestionInstance to construct the file path.
    try:
        uq = models.UserQuestion.objects.get(template=template, user=request.user, status__in=['released', 'solved'])
#        instance = models.QuestionInstance.objects.get(template=template, user=request.user, status__in=['released', 'solved'])
    except models.QuestionInstance.DoesNotExist:
        return render_to_response('error.tpl', 
            { 'errors' : ["You don't have permission to see this file."] })
    
    files = fm.FileManager()
    contents = files.load_file(template, uq.instance)
    
    return render_to_response('show_file.tpl', { 'data' : contents }, mimetype='text/plain')

@login_required
def check_q(request, template_id):
    json_response = {}
    try:
        answer = str(request.POST['answer']).strip()

        try:
            template = models.QuestionTemplate.objects.get(id=int(template_id))
            user_q = models.UserQuestion.objects.exclude(status='retired').get(user=request.user, template=template)
            q_instance = user_q.instance
        except models.QuestionTemplate.DoesNotExist:
            json_response['error'] = 'Invalid template ID.'
            return json_response
        except models.UserQuestion.DoesNotExist:
            json_response['error'] = 'The requested question is not available.'
            return json_response
        
        question_p = provider.getQuestionProvider()
        response = question_p.submit_attempt(q_instance.id, request.user.id, answer)
        
        # If correct, change the status of the question and select a next candidate.
        # Make sure that the question hasn't been solved already!
        if response.correct and user_q.status != 'solved':
            user_q.status = 'solved'
#            user_q.save()
            
            json_response['correct'] = True
            json_response['status'] = 'solved'            
            try:
                question_m = qm.QuestionManager()
                # Activate the next question.
                question_m.activate_next(request.user)
            except exception.NoQuestionReadyException:
                # TODO cartland: Should we record this?
                pass
        else:
            json_response['correct'] = response.correct
            
        return HttpResponse(json.dumps(json_response), mimetype='application/json')
        
    # Either the QID or the answer value wasn't set.
    except KeyError:
        json_response['error'] = 'Please provide a guess.'
        return HttpResponse(json.dumps(json_response), mimetype='application/json')
    except exception.UnauthorizedAttemptException:
        json_response['error'] = "You don't have permission to view that question yet."
        return HttpResponse(json.dumps(json_response), mimetype='application/json')


