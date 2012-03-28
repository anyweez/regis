from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.template import Context

from django.contrib.auth.decorators import login_required

import urllib2 # for Django requests to third party servers 
import json, datetime
import face.util.UserStats as UserStats
import face.models.models as models
import face.msg.msghub as msghub
import face.util.exceptions as exception
import face.util.QuestionManager as qm
import face.modules.providers.Provider as provider


QUESTION_SERVER = 'http://localhost:7070/question_server_stub'

########################################################
###   GET/POST   /api/questions                 ########
########################################################
def api_questions(request):
    if request.method == 'GET':
        questions = load_visible_questions(request)
        return HttpResponse(json.dumps(questions), mimetype='application/json')
    if request.method == 'POST':
        return None
    
def load_visible_questions(request):
    visible_questions = []
    questions = load_questions(request)
    for question in questions:
        if user_has_question_permission(request.user, question['question_id']):
            visible_questions.append( question )
    return visible_questions
    
def load_questions(request):
    def get_status(question):
        if question['answerable']:
            return 'released'
        elif question['gradable']:
            return 'gradable'
        return 'unknown'
    question_p = provider.getQuestionProvider()
    questions = question_p.get_questions(request.user.id)
    
#    url = QUESTION_SERVER + '/questions'
#    f = urllib2.urlopen(url, None, 5000)
#    third_party_questions = json.loads(f.read())
#    question_tpl = get_template('question.tpl')
#    for third_party_question in third_party_questions:
#        question = {
#            'status' : get_status(third_party_question),
#            'question_id' : third_party_question['id'],
#            'decoded_text' : third_party_question['content'],
#            'time_released' : 'Today',
#            'gradable' : third_party_question['gradable'],
#            'answerable' : third_party_question['answerable'],
#        }
#        question['html'] = question_tpl.render(Context( {
#            'question' : question
#        } ))
#        questions.append(question) 
    return questions

''' TODO(cartland): Complete stub '''
def user_has_question_permission(user, question_id):
    return True
    squestions = models.ServerQuestion.objects.filter(question_id=question_id)
    for q in squestions:
        if len(q.users.filter(id=user.id)) > 0:
            return True
    return False

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
        decks = load_visible_decks(request)
        return HttpResponse(json.dumps(decks), mimetype='application/json')
    return None
    
def load_visible_decks(request):
    visible_decks = []
    decks_resource = load_decks(request)
    for deck in decks_resource:
        if user_has_deck_permission(request.user, deck):
            visible_decks.append(deck)
    return visible_decks

''' Database lookup or API request '''
def load_decks(request):
    decks = []
    db_decks = models.Deck.objects.all()
    for db_deck in db_decks:
        deck = get_deck_from_db_deck(request, db_deck)
        decks.append(deck)
    return decks

def get_deck_from_db_deck(request, db_deck):
    question_ids_list = load_question_ids_from_deck(request, db_deck)
    deck = {
        "deck_id" : db_deck.id,
        "name" : db_deck.name,
        "questions" : question_ids_list,
        "shared_with" : db_deck.shared_with,
    }
    return deck

''' TODO(cartland): Complete stub '''
def user_has_deck_permission(user, deck):
    return True
    db_decks = models.Deck.objects.filter(id=deck['deck_id'])
    if 0 < len(db_decks.users.filter(id=user.id)):
        return True
    elif 0 < len(models.Deck.objects.filter(shared_with='public')):
        return True
    return False

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
        deck = delete_visible_deck(request, deck_id)
        return HttpResponse(json.dumps(deck), mimetype='application/json')
    return None
        

def load_visible_deck(request, deck_id):
    deck = load_deck(request, deck_id)
    if user_has_deck_permission(request.user, deck):
        return deck
    return None

def delete_visible_deck(request, deck_id):
    deck = load_deck(request, deck_id)
    if user_has_deck_permission(request.user, deck):
        return delete_deck(request, deck_id)
    return None

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
# PUT /api/decks/{{deck_id}}/questions/{{question_id}} ##
########################################################

########################################################
#           DELETE /api/decks/{{deck_id}}              #
########################################################

########################################################
#   POST /api/decks/{{deck_id}}/union/{{deck_id}}      #
########################################################

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
    cards.append({'card_id' : 123, 'html' : login_card.render(Context()) })
    cards.append({'card_id' : 423, 'html' : howitworks_card.render(Context()) })
    cards.append({'card_id' : 7823, 'html' : about_card.render(Context()) })
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



