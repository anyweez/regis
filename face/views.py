from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import math, datetime
import models.models as users
import util.QuestionManager as util
import msg.msghub as msghub
import util.exceptions as exception

import re, json, hashlib
from face.util.QuestionManager import QuestionManager

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
    if request.user.is_authenticated():
        return redirect('/dash')
    else:
        return render_to_response('index.tpl', 
            { 'errors' : msghub.get_printable_errors() }, 
            context_instance=RequestContext(request))

@login_required
def build_acct(request):
    try:
        users.RegisUser.objects.get(user=request.user)
    except users.RegisUser.DoesNotExist:
        print 'building new user account!'
        # Update the user's username.
        u = request.user
        u.username = '%s %s' % (u.first_name, u.last_name)
        u.save()

        # Create their RegisUser record.        
        league = users.RegisLeague.objects.get(id=1)
        
        ruser = users.RegisUser(user=u, league=league)
        ruser.save()
        
        # Good to go!
        
    return redirect('/dash')

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
'''
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
'''

def authsub(request):
    pass

@login_required
def dash(request):
    qm = util.QuestionManager()
    current_q = None
    
    try:
        current_q = qm.get_current_question(request.user)
        # Get the time until next release in seconds
        next_release_s = qm.time_until_next(request.user).seconds
    
        next_release = {}
        next_release['hours'] = int(math.floor(next_release_s / 3600))
        next_release_s -= (next_release['hours'] * 3600)
        next_release['minutes'] = int(math.floor(next_release_s / 60))
        next_release_s -= (next_release['minutes'] * 60)
    
    except exception.NoQuestionReadyException:
        next_release = None
        
    return render_to_response('dashboard.tpl', 
        { 'user': request.user, 
          'question': current_q, 
          'ttl' : next_release,
          'messages' : msghub.get_messages(),
          'errors' : msghub.get_printable_errors() },
        context_instance=RequestContext(request)
    )

def login(request):    
    if len(request.POST['username']) > 0 and len(request.POST['password']) > 0:
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        
        if user is not None:
            if user.is_active:
                ruser = user.get_profile()
                
                # Save an event recording that the user just logged in. 
                users.RegisEvent(who=ruser, event_type="login").save()
                
                auth.login(request, user)
                
                # If the user hasn't had a question released in 48 hours, release
                # a new one.
                qm = util.QuestionManager()
                try:
                    # Raises a NoQuestionReadyException if user hasn't ever had a
                    # question released.
                    currentq = qm.get_current_question(ruser)
                    last_unlock = (datetime.datetime.now() - currentq.time_released)
                    
                    # If it's been more than 2 days, release a new question.
                    if last_unlock > datetime.timedelta(days=2):
                        # Raises a NoQuestionReadyException if there are no
                        # questions left to unlock.
                        qm.activate_next(ruser)
                except exception.NoQuestionReadyException:
                    try:
                        qm.activate_next(ruser)
                    # If the exception gets thrown again then there are no new questions
                    # to activate and we can just proceed.  The view logic and template
                    # code is designed to deal with this situation.
                    except:
                        pass
                    
                # Correct, let's proceed.
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
            
            qm = QuestionManager()
            # Activate the next question.
            qm.activate_next(ruser)

        return redirect('/question/status/%d' % g.id)
        
    # Either the qid, the answer, or one of the redirects wasn't set.
    except KeyError:
        pass
    except exception.UnauthorizedAttemptException:
        pass

@login_required
def list_questions(request):
    ruser = request.user.get_profile()
    all_questions = users.Question.objects.filter(uid=ruser).order_by('tid')
    
    return render_to_response('list_questions.tpl', 
        { 'questions' : all_questions,
          'user' : request.user }
    )

@login_required
def view_question(request, tid):
    ruser = request.user.get_profile()
    template = users.QuestionTemplate.objects.get(id=tid)
    
    if template is not None:
        question = users.Question.objects.filter(uid=ruser, tid=template)
    
        # If there is a question that matches their request, display it.
        if len(question) > 0:
            question = question[0]
            return render_to_response('view_question.tpl', 
                { 'question' : question, 'user': request.user },
                context_instance=RequestContext(request))
        # There is no question matching the requested data.
        else:
            # TODO: Need to return some error responses here.
            pass
    else:
        # TODO: Error response needed here as well.
        pass

@login_required
def question_status(request, gid):
    ruser = request.user.get_profile()
    try:
        guess = users.Guess.objects.get(id=gid)
        question = guess.qid
        
        # Get the information for the next question
        qm = QuestionManager()
        try:
            next_q = qm.get_current_question(ruser)
        except exception.NoQuestionReadyException:
            next_q = None
            
        answers = users.Answer.objects.filter(qid=question, value=guess.value)
        
        answer = None
        if len(answers) > 0:
            answer = answers[0]
        
        return render_to_response('question_status.tpl', 
            { 'guess' : guess, 
              'question' : question, 
              'next_q' : next_q,
              'user': request.user,
              'answer': answer },
            context_instance=RequestContext(request))
    except users.Guess.DoesNotExist:
        msghub.register_error(9, gid)
        return render_to_response('error.tpl', { 'errors' : msghub.get_printable_errors() })
    

@login_required
def get_question_file(request, tid):
    ruser = request.user.get_profile()
    templates = users.QuestionTemplate.objects.filter(id=tid)
    
    data = None
    field = []
    
    if len(templates) > 0:
        questions = users.Question.objects.filter(uid=ruser, tid=templates[0])
        
        if len(questions) > 0:
            data = json.loads(questions[0].variables)
            for actual, visible in data.values():
                try:
                    if list(actual) == actual and len(actual) > len(field):
                        field = actual
                except TypeError:
                    continue
    
    return render_to_response('show_file.tpl', { 'data' : field }, mimetype='text/plain')

@login_required
def get_all_hints(request, tid):
    try:
        template = users.QuestionTemplate.objects.get(id=tid)
        
        hints = users.QuestionHint.objects.filter(template=template)
        outlist = [hint.get_hash() for hint in hints]
        
    except users.QuestionTemplate.DoesNotExist:
        pass
    
    return HttpResponse(json.dumps(outlist), mimetype='application/json')

@login_required
def get_hint_details(request, tid, hinthash):
    try:
        template = users.QuestionTemplate.objects.get(id=tid)

        ruser = request.user.get_profile()
        try:
            hints = users.QuestionHint.objects.filter(template=template)
        
            # TODO: order the hints somehow.
        
            # Get the specific hint that we want to return.
            chosen = None
            for hint in hints:
                if hint.get_hash() == hinthash:
                    chosen = hint
                
            # Tally the votes
            votes = users.QuestionHintRating.objects.filter(hint=chosen)
        
            upvotes = 0
            downvotes = 0
            for vote in votes:
                if vote.rating:
                    upvotes += 1
                else:
                    downvotes += 1
        
            # Show all of this info.
            chosen_data = {
                'hint_id' : hinthash,
                'hint_body' : chosen.text,
                'upvotes' : upvotes,
                'downvotes' : downvotes 
            }

            # Register an event saying that the user viewed the hint.
            users.RegisEvent(event_type='gethint', who=ruser, target=chosen.id).save()
            return HttpResponse(json.dumps(chosen_data), mimetype='application/json')

        except users.Question.DoesNotExist:
            msghub.register_error(9, tid)
            return render_to_response('error.tpl', {'errors' : msghub.get_printable_errors() })
    except users.QuestionTemplate.DoesNotExist:
        msghub.register_error(9, tid)
        return render_to_response('error.tpl', {'errors' : msghub.get_printable_errors() })
        
        
@login_required
def submit_hint(request, tid):
    template = users.QuestionTemplate.objects.get(id=tid)
    ruser = request.user.get_profile()
    # Save the hint!
    try:
        user_q = users.Question.objects.get(tid=template, uid=ruser)
        prev_hints = users.QuestionHint.objects.filter(template=template, src=ruser)

        # Check that the problem has been solved and that the user hasn't provided
        # any hints for this question already.
        if user_q.status == 'solved' and len(prev_hints) is 0:
            users.QuestionHint(template=template, src=ruser, text=request.POST['hinttext']).save()
            msghub.register_message('Thanks for providing a hint!', template, True)
        # Error: the user has already provided a hint.
        elif len(prev_hints) is 0:
            msghub.register_error(8, template)
        # Error: the user hasn't answered the question yet.
        else:
            msghub.register_error(7, template)
    except users.Question.DoesNotExist:
        msghub.register_error(7, template)
        
    return redirect('/dash')

def tally_vote(request, hinthash, vote):
    hints = users.QuestionHint.objects.all()
    ruser = request.user.get_profile()

    # Get the specific hint that we want to return.
    chosen = None
    for hint in hints:
        if hint.get_hash() == hinthash:
            chosen = hint
    
    # Check to make sure that the user hasn't 
    prev_ratings = users.QuestionHintRating.objects.filter(hint=chosen, src=request.user.get_profile())
    if len(prev_ratings) > 0:
        approval = prev_ratings[0].rating
        if approval:
            response = { 'msg' : "You've already upvoted this hint." }
        else:
            response = { 'msg' : "You've already downvoted this hint." }
    elif chosen is None:
        response = { 'msg' : 'Invalid hint.' }
    else:
        ratings = users.QuestionHintRating.objects.filter(hint=chosen)
        upvotes = 0
        downvotes = 0
        
        for rating in ratings:
            if rating.rating:
                upvotes += 1
            else:
                downvotes += 1
    
        if vote:
            rating = 1
            upvotes += 1
        else:
            rating = 0
            downvotes += 1
    
        response = { 'msg' : 'success', 'upvotes' : upvotes, 'downvotes' : downvotes }
        users.QuestionHintRating(hint=chosen, src=ruser, rating=rating).save()
    
    return HttpResponse(json.dumps(response), mimetype='application/json')