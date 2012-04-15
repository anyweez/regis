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
    released = models.DateTimeField(auto_now_add=False, null=True)
    
    order = models.SmallIntegerField()
    
    visible = models.BooleanField()
    answerable = models.BooleanField()
    status = models.CharField(max_length=10, choices=REGIS_QUESTION_STATUS)

    def jsonify(self):
        return { 
            'user' : self.user.id,
            'template_id' : self.template.id,
#            'released' : self.released,
#            'visible' : self.visible,
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
    question = models.ForeignKey(UserQuestion)
    
    value = models.CharField(max_length=100)
    correct = models.BooleanField()
    time_guessed = models.DateTimeField()

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

# A collection of QuestionTemplates.  Decks can be created by users
# and QuestionTemplates can be added / removed.  They can also be
# shared with others.
class Deck(models.Model):
    # TODO: I think this needs an 'owner' field (luke)...why the users field again?
    questions = models.ManyToManyField('QuestionTemplate')
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=100)
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
