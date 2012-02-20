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

@login_required
def about(request):
    return render_to_response('about.tpl', { 'user' : request.user })

def howitworks(request):
    return render_to_response('howitworks.tpl')

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

        # Create their RegisUser record.  
        # TODO: id=1 shouldn't be hard-coded here.      
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
                
        u.save()
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
        next_release_s = question_m.time_until_next(request.user).total_seconds()
        
        print next_release_s
        # Release a question if they've passed their deadline.
        if next_release_s < 0:
            question_m.activate_next(request.user)
            next_release_s = question_m.time_until_next(request.user).seconds
    # If that doesn't work, try to activate a new question.  This should work
    # unless there are no questions left to activate.
    except exception.NoQuestionReadyException:
        try:
            question_m.activate_next(request.user)
            
            next_release = {}
            next_release_s = question_m.time_until_next(request.user).seconds
        # If there are no more questions to activate, let them know that.  There's
        # nothing more we can do!
        except exception.NoQuestionReadyException:
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
        try:
            question = users.Question.objects.get(id=qid, user=request.user)
        except users.Question.DoesNotExist:
            raise exception.UnauthorizedAttemptException(request.user, qid)
        
        question_m = qm.QuestionManager()
        correct, msg = question_m.check_question(question, answer)
        
        msghub.register_message(msg, target=qid, status=correct)
        
        # Record the guess.
        g = users.Guess(user=request.user, 
                        question=question, 
                        value=answer, 
                        correct=correct, 
                        time_guessed=datetime.datetime.now())
        g.save()
        
        # If correct, change the status of the question and select a next candidate.
        # Make sure that the question hasn't been solved already!
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
        return redirect('/question/status/%d' % g.id)
        
    # Either the qid, the answer, or one of the redirects wasn't set.
    except KeyError:
        pass
    except exception.UnauthorizedAttemptException:
        pass

@login_required
def list_questions(request):
    qs = users.QuestionSet.objects.get(reserved_by=request.user)
    all_questions = qs.questions.exclude(status='retired').order_by('template')
    
    # Compute statistics for # solved vs. # available on the fly.  We
    # may want to batch this later if performance becomes an issue.  It
    # won't scale particularly well as the user load increases.
    for question in all_questions:
        available = users.Question.objects.filter(template=question.template).exclude(status='retired')
        question.num_available = sum([1 for q in available if q.status in ('released', 'solved')])
        question.num_solved = sum([1 for q in available if q.status == 'solved'])
        if question.num_available > 0:
            question.solved_percent = (question.num_solved * 1.0 / question.num_available) * 100
        else:
            question.solved_percent = 0.0
    
    return render_to_response('list_questions.tpl', 
        { 'questions' : all_questions,
          'stats' : UserStats.UserStats(request.user),
          'user' : request.user }
    )

@login_required
def view_question(request, tid):
    try:
        template = users.QuestionTemplate.objects.get(id=tid)
        question = users.Question.objects.exclude(status='retired').get(user=request.user, template=template)

        print question.id

        return render_to_response('view_question.tpl', 
            { 'question' : question, 
              'stats' : UserStats.UserStats(request.user),
              'user': request.user },
              context_instance=RequestContext(request))
    except users.QuestionTemplate.DoesNotExist:
        # TODO: Need to return some error responses here.
        pass
    except users.Question.DoesNotExist:
        # There is no question matching the requested data.
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
    try:
        template = users.QuestionTemplate.objects.get(id=tid)
    
        data = None
        field = []

        try:
            questions = users.Question.objects.filter(user=request.user, templates=template).exclude(status='retired')
            data = json.loads(questions[0].variables)
            for actual, visible in data.values():
                try:
                    if list(actual) == actual and len(actual) > len(field):
                        field = actual
                except TypeError:
                    continue
        except users.Question.DoesNotExist:
            pass
    except users.QuestionTemplate.DoesNotExist:
        pass
    
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
        user_q = users.Question.objects.get(template=template, user=request.user).exclude(status='retired')
        prev_hints = users.QuestionHint.objects.filter(template=template, src=request.user)

        # Check that the problem has been solved and that the user hasn't provided
        # any hints for this question already.
        if user_q.status == 'solved':# and len(prev_hints) is 0:
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

@login_required
def feedback_like(request, tid, value):
    try:
        template = users.QuestionTemplate.objects.get(id=tid)
        preexisting = users.QuestionFeedback.objects.get(user=request.user, template=template, category='like')
    
        if value != preexisting.value:
            preexisting.value = value
            preexisting.save()
    # This is an error resulting from a malformed URL.
    except users.QuestionTemplate.DoesNotExist:
        print "Template doesn't exist."
        pass
    except users.QuestionFeedback.DoesNotExist:
        fb = users.QuestionFeedback(user=request.user, template=template, category='like', value=value)
        fb.save()
        
    return render_to_response('empty.tpl')

def feedback_challenge(request, tid, value):
    try:
        template = users.QuestionTemplate.objects.get(id=tid)
        preexisting = users.QuestionFeedback.objects.get(user=request.user, template=template, category='challenge')
    
        if value != preexisting.value:
            preexisting.value = value
            preexisting.save()
    # This is an error resulting from a malformed URL.
    except users.QuestionTemplate.DoesNotExist:
        print "Template doesn't exist."
        pass
    except users.QuestionFeedback.DoesNotExist:
        fb = users.QuestionFeedback(user=request.user, template=template, category='challenge', value=value)
        fb.save()
        
    return render_to_response('empty.tpl')

@login_required
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


@login_required
def suggest_q(request):
    return render_to_response('suggest_q.tpl', { 'user': request.user },
                              context_instance=RequestContext(request))
    
@login_required
def submit_suggestion(request):
    sugg_q = str(request.POST['question'])
    ans = str(request.POST['answer'])

    # Record the suggestion.
    s = users.Suggestion(user=request.user, question=sugg_q, answer=ans, time_submitted=datetime.datetime.now())
    s.save()
    msghub.register_message('Thanks for submitting a question!')
        
    return redirect('/dash')

def questions_unknown(request):
    return redirect('/questions/list')

def list_questions_with_api(request):
    return render_to_response('questions_list.tpl', 
          { 'stats' : UserStats.UserStats(request.user),
          'user': request.user },
           context_instance=RequestContext(request))

@login_required
def view_question_with_api(request, tid):
    return render_to_response('questions_view.tpl', 
                { 'tid' : tid, 
                  'stats' : UserStats.UserStats(request.user),
                  'user': request.user },
                context_instance=RequestContext(request))


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
            response['html'] = render_to_response('questions_get.tpl',
                                { 'questionstatus' : "doesnotexist",
                                  'questiontitle' : "Question not found",
                                  'questionnumber' : question_id,
                                  'questioncontent' : "This question does not exist. Contact us if you think this is a mistake.",
                                  'questionpublished' : "",
                                  'hintsids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'thumbnail':
            response['html'] = render_to_response('questions_get_thumbnail.tpl',
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
            response['html'] = render_to_response('questions_get.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : "Oops, this questions is locked. Keep working and you'll be here soon!",
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : [] },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'thumbnail':
            response['html'] = render_to_response('questions_get_thumbnail.tpl',
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
            response['html'] = render_to_response('questions_get_thumbnail.tpl',
                                { 'questionstatus' : question.status,
                                  'questiontitle' : question.template.title,
                                  'questionnumber' : question.template.id,
                                  'questioncontent' : question.decoded_text(),
                                  'questionpublished' : str(question.time_released),
                                  'hintids' : hintids },
                                context_instance=RequestContext(request)
                              ).content
        elif options['html'] == 'full':
            response['html'] = render_to_response('questions_get.tpl',
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
    response['html'] = render_to_response('hints_get.tpl',
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
def api_attempts_insert(request, qid):
    errors = []
    question_id = qid
    content = "sample"
    if False: # DEBUG
        if request.method != 'POST':
            return HttpResponse(json.dumps({ "kind" : "Expecting POST request" }),
                                mimetype='application/json')
        if 'question' in request.POST:
            question_id = int(request.POST['question'])
            if question_id != qid:
                errors.append("Question id does not match");
        else:
            errors.append("No question given")
        if 'content' in request.POST:
            content = request.POST['content']
            if len(content) == 0:
                errors.append("No content given")
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
        raise exception.UnauthorizedAttemptException(request.user, qid)
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
    
    msghub.register_message(msg, target=qid, status=correct)
    
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
                 "html" : attempt.value,
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
def system_tests_run(request):
    def is_system_authorized():
        return request.user.id == 2
    if not is_system_authorized():
        return HttpResponse(json.dumps({'kind' : 'unauthorized'}), mimetype='application/json')
    tests = [
        ['questions_get', 'generic_api_test', 
         {
         'api_method' : 'api.questions.get',
         'num_args' : '1',
         'args_list' : [1],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
             'kind' : 'question',
             'key' : 181,
             'id' : 1,
             'hints' : None,
             'errors' : None,
             'title' : 'Numbers in Numbers',
             'url' : 'http://localhost:8080/questions/1',
             'actor' : 2,
             'content' : None,
             'html' : None,
             'published' : None,
             'status' : None,
           })
         }],

        ['questions_list', 'generic_api_test',
         {
         'api_method' : 'api.questions.list',
         'num_args' : '0',
         'args_list' : [],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
             'kind' : 'questionFeed',
             'items' : None,
           })
         }],

        ['test_hints_get', 'generic_api_test',
         {
         'api_method' : 'api.hints.get',
         'num_args' : '1',
         'args_list' : [1],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
           "rating": 5,
           "kind": "hint",
           "question": 1,
           "actor": 2,
           "content": "How would you find the sum of the first five? And then the next five?",
           "html": None,
           "id": 1,
           }),
         }],

        ['fail_guess_get', 'generic_api_test',
         {
         'api_method' : 'api.attempts.get',
         'num_args' : '1',
         'args_list' : [1],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
           "kind": "attempt",
           "id": 1,
           "content": "Attempt",
           "attempt_index": None,
           "question": 1,
           "correct" : False,
           "url" : None,
           "actor": 2,
           "html": None,
           "published": None,
           }),
         }],

        ['fail_guess_insert', 'generic_api_test',
         {
         'api_method' : 'api.attempts.insert',
         'num_args' : '2',
         'args_list' : [4, "sample"],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
           "kind": "attempt",
           "id": None,
           "content": "sample",
           "attempt_index": None,
           "question": 4,
           "correct" : False,
           "url" : None,
           "actor": 2,
           "html": None,
           "published" : None,
           }),
         }],

        ['attemps_list_structure', 'generic_api_test',
         {
         'api_method' : 'api.attempts.list',
         'num_args' : '1',
         'args_list' : [4],
         'no_more_fields' : 'true',
         'expected_response' : json.dumps({
           "kind": "attemptFeed",
           "question": 4,
           "items" : None,
           }),
         }],
    ]
    return render_to_response('system_tests_run.tpl',
        { 'tests' : tests,
          'wait_for_click' : 'no' }, 
          context_instance=RequestContext(request)
        )




