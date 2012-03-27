from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth.decorators import login_required

import urllib2 # for Django requests to third party servers 
import json, datetime
import face.util.UserStats as UserStats
import face.models.models as models
import face.msg.msghub as msghub
import face.util.exceptions as exception
import face.util.QuestionManager as qm



QUESTION_SERVER = 'http://localhost:8090/api/question_server_stub'

def api_questions(request):
    questions = load_visible_questions()
    return HttpResponse(json.dumps(questions), mimetype='application/json')
    
def load_visible_questions():
    visible_questions = []
    questions_resource = load_questions()
    for question in questions_resource:
        if user_has_question_permission(None, question):
            visible_questions.append(question)
    return visible_questions

def load_questions():
    url = QUESTION_SERVER + '/questions'
    f = urllib2.urlopen(url, None, 5000)
    return json.loads(f.read())

''' TODO(cartland): Complete stub '''
def user_has_question_permission(user, question):
    return True
    #return 1 == len(question.users.filter(id=user.id))

def api_decks(request):
    decks = load_visible_decks()
    return HttpResponse(json.dumps(decks), mimetype='application/json')
    
def load_visible_decks():
    visible_decks = []
    decks_resource = load_decks()
    for deck in decks_resource:
        if user_has_deck_permission(None, deck):
            visible_decks.append(deck)
    return visible_decks

''' Database lookup or API request '''
def load_decks():
    decks_resource = []
    decks = models.Deck.objects.all()
    for deck in decks:
        question_ids_list = load_question_ids_from_deck(deck)
        decks_resource.append( {
            "id" : deck.id,
            "name" : deck.name,
            "questions" : question_ids_list,
        } )
    return json.loads(decks_resource)

''' TODO(cartland): Complete stub '''
def user_has_deck_permission(user, deck):
    return True
    #return len(deck.users.filter(id=user.id))

''' TODO(cartland): Deck needs questions=ManyToMany(Question) 
Deck needs question_id=???'''
def load_question_ids_from_deck(deck):
    question_ids = []
    for regis_question in deck.questions:
        if user_has_question_permission(None, regis_question.question_id):
            question_ids.append(regis_question.question_id)
    return question_ids

def api_deck(request, deck_id):
    deck = load_visible_deck(deck_id)
    return HttpResponse(json.dumps(deck), mimetype='application/json')

def load_visible_deck(deck_id):
    deck = load_deck(deck_id)
    if user_has_deck_permission(user, deck):
        return deck
    return None

''' Database lookup or API request '''
def load_deck(deck_id):
    deck = models.Deck.objects.get(deck_id)
    question_ids_list = load_question_ids_from_deck(deck)
    deck_resource = {
        "id" : deck.id,
        "name" : deck.name,
        "questions" : question_ids_list,
    } 
    return json.loads(decks_resource)

@login_required
def get_users(request):
    personal = get_template('profile.tpl')

    cards = []
    cards.append({ 'html' : personal.render(Context({'user':request.user})) })
    return HttpResponse(json.dumps(cards), mimetype='application/json')

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



