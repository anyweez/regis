from django.db import models
from django.contrib.auth.models import User

import json, re

REGIS_SHARING_OPTIONS = (
    ('public', 'Public'),
    ('league', 'League'),
    ('private', 'Private'),
)

REGIS_QUESTION_TYPES= (
    ('auto', 'Auto-graded'),
    ('peer', 'Peer graded')
)
    
REGIS_QUESTION_STATUS = (
    ('solved', 'Solved'),       # question has been released and answered
    ('released', 'Released'),   # question has been released but not answered
    ('ready', 'Ready'),         # question parsed and answers available, not released
    ('pending', 'Pending'),      # question parsed but answers not available
    ('retired', 'Retired')      # deactivated but not deleted (often through manage.py refresh)
)

REGIS_TEMPLATE_STATUS = (
    ('waiting', 'Waiting'),      # not yet parsed
    ('pending', 'Pending'),     # parsed, not answered
    ('ready', 'Ready')          # parsed and answered
)

######################################
###### Question-related models #######
######################################

# A single QuestionTemplate exists per question.  The template
# ID is how questions are identified externally.
#
# QuestionTemplates are used to store the pre-parsed question,
# including questions that don't have any parsing variables in
# them.
class QuestionTemplate(models.Model):
    type = models.CharField(max_length=10, choices=REGIS_QUESTION_TYPES)
    text = models.TextField()
    owner = models.ForeignKey(User)
    
    added_on = models.DateTimeField(auto_now_add=True)
    solver_name = models.CharField(max_length=40)
    
    live = models.BooleanField()
    status = models.CharField(max_length=10, choices=REGIS_TEMPLATE_STATUS)
    def jsonify(self):
        return {
            'template_id' : self.id,
            'text' : self.text,
            'type' : self.type,
            'status' : self.status,
#            'added_on' : self.added_on,
        }

    def __str__(self):
        return json.dumps(self.jsonify())

# A particular instance of a QuestionTemplate after the template
# is compiled.  There are usually many of these per question template,
# but it's also possible to have a one-to-one mapping if there aren't
# any variables in the body.
class QuestionInstance(models.Model):
    template = models.ForeignKey(QuestionTemplate)
    
    text = models.TextField()
    variables = models.TextField()
    
    generated_on = models.DateTimeField(auto_now_add=True)
    
    # Whether the question instance should be used for anything.  The only reason
    # that an instance becomes inactive is if the template that it is generated 
    # from is retired.
    active = models.BooleanField(default=True)

    def decoded_text(self):
        print 'decoding text...'
        pattern = re.compile('\[\[([a-z0-9\/]+)\]\]')
        matches = pattern.search(self.text)
        if matches is None:
            return self.text
        else:
            path = matches.group(0)[2:-2]
            text = self.text.replace(matches.group(0), '<a href="/%s">View link</a>' % path)
            return text

# A mapping between a QuestionInstance and a User.  Multiple users
# can be mapped to the same QuestionInstance, and in theory many
# QuestionInstances can be matched to a single User, although this
# doesn't make as much sense in normal cases.
#
# These records also store all user-specific information about a
# specific question, such as the order that it should appear in,
# the status of the question, and activity flags.
class UserQuestion(models.Model):
    user = models.ForeignKey(User)
    instance = models.ForeignKey(QuestionInstance)
    template = models.ForeignKey(QuestionTemplate)
    released = models.DateTimeField(auto_now_add=True, null=True)
    
    order = models.SmallIntegerField()
    
    visible = models.BooleanField(default=True)
    answerable = models.BooleanField(default=True)
    gradable = models.BooleanField()
    status = models.CharField(max_length=10, choices=REGIS_QUESTION_STATUS)

    def jsonify(self):
        return { 
            'user' : self.user.id,
            'question_id' : self.template.id,
            'card_id' : self.template.id,
            'order' : self.order,
            'released' : self.released.isoformat(),
            'visible' : self.visible,
            'answerable' : self.answerable,
            'gradable' : self.gradable,
            'text' : self.instance.decoded_text(),
            'status' : self.status
            }
    def __str__(self):
        return json.dumps(self.jsonify())

# Not currently implemented.
#
# QuestionTags will be used to loosely categorize questions, either
# publicly or privately.
class QuestionTag(models.Model):
    name = models.CharField(max_length=100)

# Stores a single guess from a user, both for correct and incorrect
# guesses.
class Guess(models.Model):
    user = models.ForeignKey(User)
    instance = models.ForeignKey(QuestionInstance)
    
    value = models.CharField(max_length=500)
    correct = models.BooleanField()
    time_guessed = models.DateTimeField(auto_now_add=True)
    
    def jsonify(self):
        return {
            'attempt_id' : self.id,
            'user_id' : self.user.id,
            'question_id' : self.instance.template.id,
            'text' : self.value,
            'correct' : self.correct,
            'time_guessed' : self.time_guessed.isoformat(),
        }

# Stores answers for particular QuestionInstances, whether the answer
# is correct or not.  Specific incorrect answers can be stored by
# solvers if custom messages should be presented when the answer is
# provided.
class Answer(models.Model):
    question = models.ForeignKey(QuestionInstance)
    correct = models.BooleanField()
    
    value = models.CharField(max_length=100)
    message = models.CharField(max_length=200, null=True)
    
    time_computed = models.DateTimeField(auto_now_add=True)
    
    def jsonify(self):
        return { 
            'answer_id' : self.id,
            'question_id' : self.question.template.id,
            'correct' : self.correct,
            'text' : self.value,
            'message' : self.message,
            'time_computed' : self.time_computed.isoformat()
        }


class EvaluationMessage(models.Model):
    message = models.CharField(max_length=500)
    
    def stringify(self):
        return self.message

class GuessEvaluation(models.Model):
    # The evaluator.
    author = models.ForeignKey(User, related_name='author')
    # The person who wrote the answer that is being evaluated.
    guesser = models.ForeignKey(User, related_name='guesser')
    attempt = models.ForeignKey(Guess, related_name='attempt')

    messages = models.ManyToManyField(EvaluationMessage)
    
    score = models.IntegerField()
    time_guessed = models.DateTimeField(auto_now_add=True)
    def jsonify(self):
        return {
            'id' : self.id,
            'attempt' : self.attempt.id,
            'author' : self.author.id,
            'guesser' : self.guesser.id,
            'score' : self.score,
            'time_guessed' : self.time_guessed.isoformat()
        }


class Hint(models.Model):
    template = models.ForeignKey(QuestionTemplate)
    author = models.ForeignKey(User)
    time_added = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500)
    
    def jsonify(self):
        return {
            'hint_id' : self.id,
            'question_id' : self.template.id,
            'author' : self.author.id,
            'text' : self.text,
        }


class HintRating(models.Model):
    hint = models.ForeignKey(Hint)
    author = models.ForeignKey(User)
    rating = models.BooleanField()
    
    def jsonify(self):
        return {
            'hint_rating_id' : self.id,
            'hint_id' : self.hint.id,
            'author' : self.author.id,
            'rating' : self.rating,
        }




# A collection of QuestionTemplates.  Decks can be created by users
# and QuestionTemplates can be added / removed.  They can also be
# shared with others.
class Deck(models.Model):
    owner = models.ForeignKey(User, related_name='owner')
    questions = models.ManyToManyField('QuestionTemplate')
    # The users field is not being used yet. This field will help define permissions. 'users' are all of the users that have explicit access to this deck. 
    # TODO: 'users' may not be required, depending on how fine-grained we want to get with this.
    users = models.ManyToManyField(User, related_name='viewers')
    name = models.CharField(max_length=100)
    # 'shared_with' is a special string to determine the general sharing category. Right now, everything is 'public'.
    shared_with = models.CharField(max_length=10, choices=REGIS_SHARING_OPTIONS)
    def jsonify(self):
        return {
            'deck_id' : self.id,
            'name' : self.name,
            'members' : [q.id for q in self.questions.all()],
            }

    def __str__(self):
        return json.dumps(self.jsonify())

######################################
####### Administrative models ########
######################################

class RegisLeague(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField()
    owner = models.ForeignKey(User)
    
    def __str__(self):
        return self.name

class RegisUser(models.Model):
    # This is how you extend the base user class.
    user = models.ForeignKey(User, unique=True)
    league = models.ForeignKey(RegisLeague)
    
    class Meta:
        permissions = (
            ('view_user_aggr', 'Can view aggregated statistics about users.'),
        )
    
REGIS_EVENT_TYPE = (
    ('login', 'Log In'),
)

class RegisEvent(models.Model):
    event_type = models.CharField(max_length=10, choices=REGIS_EVENT_TYPE)
    
    who = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)
    
    target = models.CharField(max_length=50, null=True)

# Social auth handlers.
from social_auth.signals import socialauth_registered
from social_auth.backends.facebook import FacebookBackend

# TODO: This currently doesn't work.  Not a big deal for us but would be nice to fix.
def facebook_extra_values(sender, user, response, details, **kwargs):
    user.email = response.get('email')
    return True

#socialauth_registered.connect(google_extra_values, sender=GoogleBackend)
socialauth_registered.connect(facebook_extra_values, sender=FacebookBackend)
