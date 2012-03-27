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



QUESTION_SERVER = 'http://localhost:7070/question_server_stub'

########################################################
########         /api/questions                 ########
########################################################
def api_questions(request):
    questions = load_visible_questions(request)
    return HttpResponse(json.dumps(questions), mimetype='application/json')
    
def load_visible_questions(request):
    visible_questions = []
    questions = load_questions(request)
    for question in questions:
        if user_has_question_permission(request.user, question):
            visible_questions.append( question )
    return visible_questions
    
def load_questions(request):
    def get_status(question):
        if question['answerable']:
            return 'released'
        elif question['gradable']:
            return 'gradable'
        return 'unknown'
    questions = []
    url = QUESTION_SERVER + '/questions'
    f = urllib2.urlopen(url, None, 5000)
    third_party_questions = json.loads(f.read())
    question_tpl = get_template('question.tpl')
    for third_party_question in third_party_questions:
        question = {
            'status' : get_status(third_party_question),
            'id' : third_party_question['id'],
            'decoded_text' : third_party_question['content'],
            'time_released' : 'Today',
            'gradable' : third_party_question['gradable'],
            'answerable' : third_party_question['answerable'],
        }
        question['html'] = question_tpl.render(Context( {
            'question' : question
        } ))
        questions.append(question) 
    return questions

''' TODO(cartland): Complete stub '''
def user_has_question_permission(user, question):
    return True
    q = models.ServerQuestion.objects.filter(id=question['id'])
    if len(q) == 0:
        q = models.ServerQuestion(question_id=question['id'])
        q.save()
        q.users.add(1)
        q.save()
    elif len(q) == 1:
        q = q[1]
    else:
        assert False
    q.users.add(user).save()
    return 1 == len(models.ServerQuestion.objects.filter(users__id=user.id))

########################################################
#            GET/POST /api/decks                           #
########################################################
def api_decks(request):
    if request.method == 'GET':
        decks = load_visible_decks(request)
        return HttpResponse(json.dumps(decks), mimetype='application/json')
    if request.method == 'POST':
        name = request.POST['name'] if 'name' in request.POST else 'New Deck'
        shared_with = request.POST['shared_with'] if 'shared_with' in request.POST else 'private'
        new_deck = models.Deck(name=name, shared_with=shared_with)
        new_deck.users.add(request.user)
        new_deck.save()
        load_deck(request, new_deck.id)
        return HttpResponse(json.dumps(deck), mimetype='application/json')
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
    decks_resource = []
    decks = models.Deck.objects.all()
    for deck in decks:
        question_ids_list = load_question_ids_from_deck(request, deck)
        decks_resource.append( {
            "id" : deck.id,
            "name" : deck.name,
            "questions" : question_ids_list,
        } )
    return json.loads(decks_resource)

''' TODO(cartland): Complete stub '''
def user_has_deck_permission(user, deck):
    return True
    if 1 == len(models.Deck.objects.filter(users__id=user.id)):
        return True
    elif 1 == len(models.Deck.objects.filter(shared_with='public')):
        return True
    return False

''' TODO(cartland): Deck needs questions=ManyToMany(Question) 
Deck needs question_id=???'''
def load_question_ids_from_deck(request, deck):
    question_ids = []
    for server_question in deck.questions:
        if user_has_question_permission(request.user, server_question.question_id):
            question_ids.append(server_question.question_id)
    return question_ids

########################################################
########       /api/deck/{{deck_id}}            ########
########################################################
def api_deck(request, deck_id):
    deck = load_visible_deck(request, deck_id)
    return HttpResponse(json.dumps(deck), mimetype='application/json')

def load_visible_deck(request, deck_id):
    deck = load_deck(request, deck_id)
    if user_has_deck_permission(request.user, deck):
        return deck
    return None

''' Database lookup or API request '''
def load_deck(request, deck_id):
    deck = models.Deck.objects.get(id=deck_id)
    question_ids_list = load_question_ids_from_deck(request, deck)
    deck_resource = {
        "id" : deck.id,
        "name" : deck.name,
        "questions" : question_ids_list,
    } 
    return decks_resource

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
def fakelist(response):
    info = []
    info.append({'id': 0, 'title': 'First Q', 'text': 'Why are we here?'})
    info.append({'id': 1, 'title': 'Second Q', 'text': 'What is recursion?'})
    info.append({'id': 2, 'title': 'Third Q', 'text': 'Who is the president of the United States?'})
    info.append({'id': 3, 'title': 'Fourth Q', 'text': 'How many Twitter followers do I have?'})
    info.append({'id': 4, 'title': 'Fifth Q', 'text': 'How many Twitter followers do you have?'})
    info.append({'id': 5, 'title': 'Sixth Q', 'text': 'Why do I have so many more Twitter followers than you?'})
    info.append({'id': 6, 'title': 'Seventh Q', 'text': 'Wait what is Twitter?'})
    return HttpResponse(json.dumps(info), mimetype='application/json')

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
    
    decks.append({'name' : 'First Wave', 'members' : [2, 4]})
    decks.append({'name' : 'Second Wave', 'members' : [2, 4, 7]})

    return HttpResponse(json.dumps(decks), mimetype='application/json')

def get_questions(request):
    cards = []
    return HttpResponse(json.dumps(cards), 
                mimetype='application/json')
    


def test_third_party_latency(request):
    url = request.GET['url']
    f = urllib2.urlopen(url)
    return HttpResponse(f.read())



