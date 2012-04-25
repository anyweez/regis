import face.models.models as models
import face.util.QuestionManager as qm
import Provider as provider

import datetime

## Note: this method should always return a list of JSON objects.
def get_decks(user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        raise provider.ProviderException('The specified user does not exist.')

#    delete_empty_decks(user_id)

    db_decks = models.Deck.objects.filter(owner=user)

    return [d.jsonify() for d in db_decks]

def add_question_to_deck(template_id, deck_id):
    template = models.QuestionTemplate.objects.get(id=template_id)
    try:
        db_deck = models.Deck.objects.get(id=deck_id)
    except models.Deck.DoesNotExist:
        db_deck = models.Deck(name="Untitled")
        db_deck.save()
    
    db_deck.questions.add(template)
    db_deck.save()

    return db_deck.jsonify()


def remove_question_from_deck(template_id, deck_id):
    template = models.QuestionTemplate.objects.get(id=template_id)
    try:
        db_deck = models.Deck.objects.get(id=deck_id)
    except models.Deck.DoesNotExist:
        return []
    
    db_deck.questions.remove(template)
    db_deck.save()
     
    return db_deck.jsonify()

def update_deck_name(deck_id, name):
    db_deck = models.Deck.objects.get(id=deck_id)
    db_deck.name = name
    db_deck.save()

def create(owner, name="Untitled", shared_with="public"):
    db_deck = models.Deck(name=name, owner=owner)
    db_deck.save()
    return db_deck.jsonify()

def delete_empty_decks(user_id):
    db_decks = models.Deck.objects.filter(owner__id=user_id)
    for d in db_decks:
        if len(d.questions.all()) == 0:
            d.delete()


