from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template

from django.contrib.auth.decorators import login_required

import socket, urllib, urllib2 # for Django requests to third party servers 
import json, datetime
import face.util.UserStats as UserStats
import face.models.models as models
import face.msg.msghub as msghub
import face.util.exceptions as exception
import face.util.QuestionManager as qm
import face.modules.providers.Provider as provider


QUESTION_SERVER = 'http://localhost:7070/question_server_stub'
socket.setdefaulttimeout(5)

########################################################
###   GET/POST   /api/questions                 ########
########################################################
def api_questions(request):
    if request.method == 'POST' or \
            ('POST' in request.REQUEST and request.REQUEST['POST'] == 'DEBUG'):
        question = create_new_question(request)
        return HttpResponse(json.dumps(question), mimetype='application/json')
    if request.method == 'GET':
        questions = load_visible_questions(request)

        for i, question in enumerate(questions):
            questions[i]['html'] = get_template('question.tpl').render(Context({'question': question}))
        
        return HttpResponse(json.dumps(questions), mimetype='application/json')
    if request.method == 'POST':
        return None
    
def load_visible_questions(request):
    visible_questions = []
    questions = load_questions(request)
    return questions
# TODO: Temporarily disabled.
#    for question in questions:
#        if user_has_question_permission(request.user, question['question_id']):
#            visible_questions.append( question )
#    return visible_questions
    
def load_questions(request):
    question_p = provider.getQuestionProvider()
    questions = [q for q in question_p.get_questions(request.user.id) if q['status'] in ['released', 'solved']]
    return questions

def get_question_from_third_party_question(third_party_question):
    question_tpl = get_template('question.tpl')
    def get_status(question):
        if question['answerable']:
            return 'released'
        elif question['gradable']:
            return 'gradable'
        return 'unknown'
    question = {
        'status' : get_status(third_party_question),
        'question_id' : third_party_question['question_id'],
        'decoded_text' : third_party_question['content'],
        'time_released' : 'Today',
        'gradable' : third_party_question['gradable'],
        'answerable' : third_party_question['answerable'],
    }
    question['html'] = question_tpl.render(Context( {
        'question' : question
    } ))
    try:
        db_question = models.ServerQuestion.objects.get(question_id=question['question_id'])
        question['shared_with'] = db_question.shared_with
    except models.ServerQuestion.DoesNotExist:
        db_question = models.ServerQuestion(question_id=question['question_id'], shared_with='private')
        db_question.save()
        question['shared_with'] = db_question.shared_with
#    models.ServerQuestion.objects.all().delete() # DELETE ALL QUESTIONS!!!
    return question

''' TODO(cartland): Complete stub '''
def user_has_question_permission(user, question_id):
    try:
        db_question = models.ServerQuestion.objects.get(question_id=question_id)
        try:
          db_question.users.get(id=user.id)
          return True
        except models.User.DoesNotExist:
          return 'public' == db_question.shared_with 
    except models.ServerQuestion.DoesNotExist as e:
        return False

def create_new_question(request):
    keys = [
        ('kind', 'freeresponsequestion', lambda s: s), 
        ('content', 'New question content', lambda s: s), 
        ('author', request.user.id, lambda s: int(s)), 
        ('answers', [], lambda s: s.split(',')), 
        ('rubricsuggestions', [], lambda s: s.split(',')), 
        ('max_score', 1, lambda s: int(s)), 
        ('shared_with', 'public', lambda s: s),
        ('answerable', True, lambda s: s),
        ('gradable', False, lambda s: s),
    ]
    values = {}
    for key, default, converter in keys:
        values[key] = converter(request.REQUEST[key]) if key in request.REQUEST else default
    question = request_new_question(values)
    return question

def request_new_question(values):
    url = QUESTION_SERVER + '/questions'
    data = urllib.urlencode(values)

##    response = urllib2.urlopen(url, data, 5000)

#    req = urllib2.Request(url, data)
#    response = urllib2.urlopen(req)
#    third_party_question = json.loads(f.read())
    response = urllib2.urlopen(url, None, 5000)
    third_party_question = json.loads(response.read())[0]
    return get_question_from_third_party_question(third_party_question)

########################################################
#        GET/POST /api/decks                           #
########################################################
def api_decks(request):
    if request.method == 'POST' or \
            ('POST' in request.REQUEST and request.REQUEST['POST'] == 'DEBUG'):
        name = request.REQUEST['name'] if 'name' in request.REQUEST else 'New Deck'
        shared_with = request.REQUEST['shared_with'] if 'shared_with' in request.REQUEST else 'public'
        new_deck = models.Deck(name=name, shared_with=shared_with)
        new_deck.save()
        #new_deck.users.add(request.user)
        #new_deck.save()
        deck = load_deck(request, new_deck.id)
        return HttpResponse(json.dumps(deck), mimetype='application/json')
    if request.method == 'GET':
#        decks = load_visible_decks(request)
        decks = [{
            'deck_id' : 1,
            'name' : 'My Questions',
            'members' : [1933,]
        }, {
            'deck_id' : 2,
            'name' : 'Midterm Review',
            'members' : [1933, 1386, 1823]
        }, {
            'deck_id' : 3,
            'name' : 'Practice Problems',
            'members' : [1933, 1406]
        }]
        return HttpResponse(json.dumps(decks), mimetype='application/json')
    return None
    
def load_visible_decks(request):
    print 'found decks'
    visible_decks = []
    decks_resource = load_decks(request)
    return decks_resource
# TODO: Temporarily disabled.
#    for deck in decks_resource:
#        if user_has_deck_permission(request.user, deck['deck_id']):
#            visible_decks.append(deck)
#    return visible_decks

''' Database lookup or API request '''
def load_decks(request):
    decks = []
    db_decks = models.Deck.objects.all()
    for db_deck in db_decks:
        deck = get_deck_from_db_deck(request, db_deck)
        decks.append(deck)
    return decks

def get_deck_from_db_deck(request, db_deck):
# TODO: Temporarily disabled.
#    question_ids_list = load_question_ids_from_deck(request, db_deck)
    question_ids_list = [question.template_id for question in db_deck.questions.all()]
    deck = {
        "deck_id" : db_deck.id,
        "name" : db_deck.name,
        "questions" : question_ids_list,
# TODO: Temporarily disabled this field.        
#        "shared_with" : db_deck.shared_with,
    }
    return deck

''' TODO(cartland): Complete stub '''
def user_has_deck_permission(user, deck_id):
    db_deck = models.Deck.objects.get(id=deck_id)
    try:
      db_deck.users.get(id=user.id)
      return True
    except models.User.DoesNotExist:
      return db_deck.shared_with == 'public' 

''' TODO(cartland): Deck needs questions=ManyToMany(Question) 
Deck needs question_id=???'''
def load_question_ids_from_deck(request, db_deck):
    question_ids = []
    for db_question in db_deck.questions.all():
        if user_has_question_permission(request.user, server_question.question_id):
            question_ids.append(server_question.question_id)
    return question_ids

########################################################
###       GET/DELETE  /api/deck/{{deck_id}}          ###
########################################################
def api_deck(request, deck_id):
    if 'GET' == request.method:
        deck = load_visible_deck(request, deck_id)
        return HttpResponse(json.dumps(deck), mimetype='application/json')
    if 'DELETE' == request.method:
        result = delete_visible_deck(request, deck_id)
        return HttpResponse(json.dumps(result), mimetype='application/json')
    return None
        

def load_visible_deck(request, deck_id):
    if user_has_deck_permission(request.user, deck_id):
        deck = load_deck(request, deck_id)
        return deck
    return None

def delete_visible_deck(request, deck_id):
    if user_has_deck_permission(request.user, deck_id):
        result = delete_deck(request, deck_id)
    return 'Deck %d deleted' % deck_id

'''
DELETE requests are idempotent,
so we should accept requests to 
delete non-existent objects
'''
def delete_deck(request, deck_id):
    try:
        db_deck = models.Deck.objects.get(id=deck_id)
        db_deck.delete()
    except models.Deck.DoesNotExist:
        pass
    return True

''' Database lookup or API request '''
def load_deck(request, deck_id):
    db_deck = models.Deck.objects.get(id=deck_id)
    deck = get_deck_from_db_deck(request, db_deck)
    return deck

''' Database or API request '''
def delete_deck(request, deck_id):
    db_deck = models.Deck.objects.get(id=deck_id)
    de_deck.delete()
    return 'Successfully deleted'

########################################################
# PUT /api/decks/{{deck_id}}/questions/{{question_id}} #
########################################################
def api_put_question_into_deck(request, deck_id, question_id):
    deck = load_visible_deck(request, deck_id)
    if deck is not None and \
            user_has_question_permission(request.user, question_id):
        put_question_into_deck(request, deck_id, question_id)
        return deck
    return None

def put_question_into_deck(request, deck_id, question_id):
    db_deck = models.Deck.objects.get(id=deck_id)
    db_question = models.ServerQuestion.objects.get(question_id=question_id)
    db_deck.questions.add(db_question)
    db_deck.save()
    return load_deck(request, deck_id)

########################################################
#   POST /api/decks/{{deck_id}}/union/{{deck_id}}      #
########################################################
def api_deck_union(request, dest_deck_id, source_deck_id):
    source_deck = load_visible_deck(request, source_deck_id)
    if user_has_deck_permission(request.user, dest_deck_id) and \
            user_has_deck_permission(request.user, source_deck_id):
        for question_id in source_deck['questions']:
            api_put_question_into_deck(request, dest_deck_id, question_id)
        dest_deck = load_visible_deck(request, dest_deck_id)
        return HttpResponse(json.dumps(dest_deck), mimetype='application/json')
    return None

########################################################
# DELETE /api/decks/{{deck_id}}/questions/{{question_id}} #
########################################################

def get_users(request):
    personal = get_template('profile.tpl')

    cards = []
    cards.append({ 'html' : personal.render(Context({'user':request.user})) })
    return HttpResponse(json.dumps(cards), mimetype='application/json')
########################################################
#                GET /api/users/me                     #
########################################################

########################################################
#                GET /api/users/                     #
########################################################

def home_deck(response):
    login_card = get_template('login.tpl')
    about_card = get_template('about.tpl')
    howitworks_card = get_template('howitworks.tpl')
    
    cards = []
    cards.append({'card_id' : 1, 'html' : login_card.render(Context()) })
    cards.append({'card_id' : 2, 'html' : howitworks_card.render(Context()) })
    cards.append({'card_id' : 3, 'html' : about_card.render(Context()) })
    return HttpResponse(json.dumps(cards), mimetype='application/json')

def get_decks(request):
    decks = []
    
    decks.append({'deck_id': 1, 'name' : 'First Wave', 'members' : [2, 4]})
    decks.append({'deck_id': 2, 'name' : 'Second Wave', 'members' : [2, 4, 7]})

    return HttpResponse(json.dumps(decks), mimetype='application/json')

@login_required
def get_questions(request):
    cards = []
    
    questions = models.Question.objects.filter(user=request.user, status='released')
    question_tpl = get_template('question.tpl')
    
    for question in questions:
        cards.append({
          'card_id' : question.template.id,
          'html' : question_tpl.render(Context({
            'question' : question
          }))
        })
    
    return HttpResponse(json.dumps(cards), 
                mimetype='application/json')

def test_third_party_latency(request):
    url = request.GET['url']
    f = urllib2.urlopen(url)
    return HttpResponse(f.read())



