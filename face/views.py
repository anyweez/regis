from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import math, datetime
import models.models as users
import util.QuestionManager as util
import msg.msghub as msghub
import util.exceptions as exception

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
    return render_to_response('index.tpl', { 'errors' : msghub.get_printable_errors() }, context_instance=RequestContext(request))

def create_account(request):
    form = users.RegisUserForm()
  
    return render_to_response('register.tpl', { 'form' : form })
  
def store_account(request):
    form = users.RegisUserForm(request.POST)
  
    if form.is_valid():
        form.save()
     
    return render_to_response('register.tpl')

@login_required
def dash(request):
    qm = util.QuestionManager()
    try:
        next_q = qm.get_current_question(request.user)
        # Get the time until next release in seconds
        next_release_s = qm.time_until_next(request.user).seconds
    
        next_release = {}
        next_release['hours'] = int(math.floor(next_release_s / 3600))
        next_release_s -= (next_release['hours'] * 3600)
        next_release['minutes'] = int(math.floor(next_release_s / 60))
        next_release_s -= (next_release['minutes'] * 60)
    
        qdata = {
            'title' : next_q.tid.q_title,
            'text' : next_q.text,
            'id': next_q.id
        }
    except exception.NoQuestionReadyException:
        qdata = {
            'not_ready' : True
        }
        next_release = None

    return render_to_response('dashboard.tpl', 
        { 'user': request.user, 
          'question': qdata, 
          'ttl' : next_release,
          'messages' : msghub.get_messages() },
        context_instance=RequestContext(request)
    )

def login(request):    
    if len(request.POST['username']) > 0 and len(request.POST['password']) > 0:
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        
        if user is not None:
            if user.is_active:
                return redirect('/dash')
                # Correct, let's proceed
            else:
                msghub.register_error(3)
                return redirect('/')
                # Correct, but account has been deactivated
        else:
            # Username or password is incorrect.
            msghub.register_error(2)
            return redirect('/')
    else:
        msghub.register_error(1) # Register an error saying info was missing.
        # Didn't provide a username or password.
        return redirect('/')

@login_required
def check_q(request):
    try:
        qid = int(request.POST['qid'])
        answer = str(request.POST['answer'])
        
        # Check to make sure the current user is allowed to answer this question.
        qset = users.Question.objects.filter(id=qid, uid=request.user)
        if len(qset) is 0:
            raise exception.UnauthorizedAttemptException(request.user, qid)
        q = qset[0]
        
        qm = util.QuestionManager()
        correct, msg = qm.check_question(q, answer)
        
        msghub.register_message(msg, target=qid, status=correct)
        
        # Record the guess.
        ruser = users.RegisUser.objects.filter(user=request.user)[0]
        g = users.Guess(uid=ruser, qid=q, value=answer, correct=correct, time_guessed=datetime.datetime.now())
        g.save()
        
        # If correct, change the status of the question and select a next candidate.
        if correct:
            q.status = 'solved'
            q.save()
                    
            return redirect(request.POST['on_correct'])
        else:
            return redirect(request.POST['on_incorrect'])
        
    # Either the qid, the answer, or one of the redirects wasn't set.
    except KeyError:
        pass
    except exception.UnauthorizedAttemptException:
        pass

@login_required
def list_questions(request):
    ruser = users.RegisUser.objects.filter(user=request.user)[0]
    all_questions = users.Question.objects.filter(uid=ruser)
    
    return render_to_response('list_questions.tpl', 
        { 'questions' : all_questions }
    )
