from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import math, datetime
import models.models as users
import util.QuestionManager as util
import msg.msghub as msghub
import util.exceptions as exception

import re

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
    return render_to_response('index.tpl', { 'errors' : msghub.get_printable_errors() }, context_instance=RequestContext(request))

def _find_acct_errors(uname, email, pwd, lid):
    errors = []
    
    # Check the username
    if len(uname) < 3 or len(uname) > 12:
        errors.append('Username must be between 3 and 10 characters long.')
        
    # Check the email address.
    exp = re.compile('[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+')
    if re.match(exp, email) is None:
        errors.append('Please provide a valid email address.')
        
    # Check the password length.
    if len(pwd) < 6:
        errors.append('You password must be at least six characters long.')
    
    # Check that the lid is an int and that the league exists.
    if int(lid) != lid:
        errors.append('Please specify a valid league ID.')
    if len(users.RegisLeague.objects.filter(id=lid)) is 0:
        errors.append('Please specify a valid league ID.')
        
    return errors

def create_account(request):
    # TODO: This isn't the best way to do this.  Django supposedly has nice
    # form support that can take care of a lot of validation for us...we
    # should look into upgrading this to use the forms API.    
    if request.method == 'POST':
        data = request.POST.copy()
        try:
            # Check to see if the two passwords match.
            if data['password'] != data['password2']:
                raise exception.DifferingPasswordException()
            
            uname = data['username']
            email = data['email']
            pwd = data['password']
            league_id = int(data['league_id'])

            # Check for registration errors.
            acct_errors = _find_acct_errors(uname, email, pwd, league_id)
            if len(acct_errors) > 0:
                for error in acct_errors:
                    msghub.register_message(error)
                return redirect('/account/create')

            # Check to make sure that the username doesn't exist yet.
            dups = users.User.objects.filter(username=uname)
            if len(dups) > 0:
                raise exception.DuplicateNameException(uname)
            
            # Save the general profile.
            user = users.User.objects.create_user(uname, email, pwd)
            # Save the profile for this user.
            ruser = users.RegisUser(league=users.RegisLeague.objects.get(id=league_id))
            ruser.user = user
            ruser.save()
            
            msghub.register_message('Account created!', target=None, status=True)
            return redirect('/')
            
        # Some field wasn't provided.
        except KeyError:
            msghub.register_error(4, target=None)
            return redirect('/account/create')
        # Invalid type for at least one field was provided.
        except TypeError as e:
            print e
            msghub.register_error(4, target=None)
            return redirect('/account/create')
        # Two passwords didn't match.
        except exception.DifferingPasswordException:
            msghub.register_error(6, target=None)
            return redirect('/account/create')
        # The username was already taken.
        except exception.DuplicateNameException(uname):
            msghub.register_error(5, target=None)
            return redirect('/account/create')
    
    else:
        form = {
            'leagues' : [(l.id, l.name) for l in users.RegisLeague.objects.all()]
        }
        return render_to_response('register.tpl', 
            { 'form' : form,
              'messages' : msghub.get_messages(),
              'errors' : msghub.get_printable_errors()
            }, context_instance=RequestContext(request))

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
                auth.login(request, user)
                # Correct, let's proceed
                return redirect('/dash')
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
def logout(request):
    auth.logout(request)
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
        
        ruser = request.user.get_profile()
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
