from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import math, datetime
import models.models as users
import util
import util.UserStats as UserStats
import util.QuestionManager as qm
import util.Concierge as question_link
import msg.msghub as msghub
import util.exceptions as exception

import re, json

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
        ruser = users.RegisUser.objects.get(user=request.user)
    except users.RegisUser.DoesNotExist:
        # Update the user's username.
        u = request.user
        u.username = '%s %s' % (u.first_name, u.last_name)
        u.save()

        # Create their RegisUser record.        
        league = users.RegisLeague.objects.get(id=1)
        
        ruser = users.RegisUser(user=u, league=league)
        ruser.save()
        
        # Activate a question set for this user.
        concierge = question_link.Concierge()
        try:
            # Allocates a question set and activates the first
            # question.
            concierge.activate_question_set(u)
        except exception.NoQuestionSetReadyException:
            msghub.register_error(10, u)
            return render_to_response('error.tpl', { 'errors' : msghub.get_printable_errors() })
                
    # Save an event recording that the user just logged in. 
    users.RegisEvent(who=request.user, event_type="login").save()
                
    # If the user hasn't had a question released in 48 hours, release
    # a new one.
    question_m = qm.QuestionManager()
    try:
        # Raises a NoQuestionReadyException if user hasn't ever had a
        # question released.  This should never happen because a new
        # question is released when the question set is assigned to
        # a user.
        currentq = question_m.get_current_question(request.user)
        last_unlock = (datetime.datetime.now() - currentq.time_released)

        # If it's been more than 2 days, release a new question.
        if last_unlock > datetime.timedelta(days=2):
            # Raises a NoQuestionReadyException if there are no
            # questions left to unlock.
            question_m.activate_next(request.user)
    except exception.NoQuestionReadyException:
        pass

    # Correct, let's proceed.
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

@login_required
def dash(request):
    question_m = qm.QuestionManager()
    current_q = None
    
    # First try to get the current question if it's already been activated.
    try:
        current_q = question_m.get_current_question(request.user)
        # Get the time until next release in seconds
        next_release = {}
        next_release_s = question_m.time_until_next(request.user).seconds
    # If that doesn't work, try to activate a new question.  This should work
    # unless there are no questions left to activate.
    except exception.NoQuestionReadyException:
        print 'activating next'
        try:
            question_m.activate_next(request.user)
            
            next_release = {}
            next_release_s = question_m.time_until_next(request.user).seconds
        # If there are no more questions to activate, let them know that.  There's
        # nothing more we can do!
        except exception.NoQuestionReadyException:
            print 'no question ready'
            next_release = None
    
    if next_release is not None:
        next_release['days'] = int(math.floor(next_release_s / 86400))
        next_release_s -= (next_release['days'] * 86400)
        next_release['hours'] = int(math.floor(next_release_s / 3600))
        next_release_s -= (next_release['hours'] * 3600)
        next_release['minutes'] = int(math.floor(next_release_s / 60))
        next_release_s -= (next_release['minutes'] * 60)
        
    return render_to_response('dashboard.tpl', 
        { 'user': request.user, 
          'question': current_q, 
          'ttl' : next_release,
          'messages' : msghub.get_messages(),
          'errors' : msghub.get_printable_errors(),
          'stats' : UserStats.UserStats(request.user),
        },
        context_instance=RequestContext(request)
    )

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
        qset = users.Question.objects.filter(id=qid, user=request.user)
        if len(qset) is 0:
            raise exception.UnauthorizedAttemptException(request.user, qid)
        q = qset[0]
        
        question_m = qm.QuestionManager()
        correct, msg = question_m.check_question(q, answer)
        
        msghub.register_message(msg, target=qid, status=correct)
        
        # Record the guess.
        g = users.Guess(user=request.user, question=q, value=answer, correct=correct, time_guessed=datetime.datetime.now())
        g.save()
        
        # If correct, change the status of the question and select a next candidate.
        if correct:
            q.status = 'solved'
            q.save()
            
            question_m = qm.QuestionManager()
            # Activate the next question.
            question_m.activate_next(request.user)

        return redirect('/question/status/%d' % g.id)
        
    # Either the qid, the answer, or one of the redirects wasn't set.
    except KeyError:
        pass
    except exception.UnauthorizedAttemptException:
        pass

@login_required
def list_questions(request):
    qs = users.QuestionSet.objects.get(reserved_by=request.user)
    all_questions = qs.questions.all().order_by('template')
    
    return render_to_response('list_questions.tpl', 
        { 'questions' : all_questions,
          'stats' : UserStats.UserStats(request.user),
          'user' : request.user }
    )

@login_required
def view_question(request, tid):
    template = users.QuestionTemplate.objects.get(id=tid)
    
    if template is not None:
        question = users.Question.objects.filter(user=request.user, template=template)
    
        # If there is a question that matches their request, display it.
        if len(question) > 0:
            question = question[0]
            return render_to_response('view_question.tpl', 
                { 'question' : question, 
                  'stats' : UserStats.UserStats(request.user),
                  'user': request.user },
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
    try:
        guess = users.Guess.objects.get(id=gid)
        question = guess.question
        
        # Get the information for the next question
        question_m = qm.QuestionManager()
        try:
            next_q = question_m.get_current_question(request.user)
        except exception.NoQuestionReadyException:
            next_q = None

        answers = users.Answer.objects.filter(question=question, value=guess.value)
        
        answer = None
        if len(answers) > 0:
            answer = answers[0]
        
        return render_to_response('question_status.tpl', 
            { 'guess' : guess, 
              'question' : question, 
              'next_q' : next_q,
              'user': request.user,
              'stats' : UserStats.UserStats(request.user),
              'answer': answer },
            context_instance=RequestContext(request))
    except users.Guess.DoesNotExist:
        msghub.register_error(9, gid)
        return render_to_response('error.tpl', { 'errors' : msghub.get_printable_errors() })
    

@login_required
def get_question_file(request, tid):
    templates = users.QuestionTemplate.objects.filter(id=tid)
    
    data = None
    field = []
    
    if len(templates) > 0:
        questions = users.Question.objects.filter(user=request.user, templates=templates[0])
        
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
            users.RegisEvent(event_type='gethint', who=request.user, target=chosen.id).save()
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
    # Save the hint!
    try:
        user_q = users.Question.objects.get(template=template, user=request.user)
        prev_hints = users.QuestionHint.objects.filter(template=template, src=request.user)

        # Check that the problem has been solved and that the user hasn't provided
        # any hints for this question already.
        if user_q.status == 'solved' and len(prev_hints) is 0:
            users.QuestionHint(template=template, src=request.user, text=request.POST['hinttext']).save()
            msghub.register_message('Thanks for providing a hint!', template, True)
        # Error: the user has already provided a hint.
        elif len(prev_hints) > 0:
            msghub.register_error(8, template)
        # Error: the user hasn't answered the question yet.
        else:
            msghub.register_error(7, template)
    except users.Question.DoesNotExist:
        msghub.register_error(7, template)
        
    return redirect('/dash')

def tally_vote(request, hinthash, vote):
    hints = users.QuestionHint.objects.all()

    # Get the specific hint that we want to return.
    chosen = None
    for hint in hints:
        if hint.get_hash() == hinthash:
            chosen = hint
    
    # Check to make sure that the user hasn't 
    prev_ratings = users.QuestionHintRating.objects.filter(hint=chosen, src=request.user)
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
        users.QuestionHintRating(hint=chosen, src=request.user, rating=rating).save()
    
    return HttpResponse(json.dumps(response), mimetype='application/json')