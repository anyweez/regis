from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

import re, hashlib

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
    
REGIS_EVENT_TYPE = (
    ('login', 'Log In'),
)

class RegisEvent(models.Model):
    event_type = models.CharField(max_length=10, choices=REGIS_EVENT_TYPE)
    
    who = models.ForeignKey(User)
    when = models.DateTimeField(auto_now_add=True)
    
    target = models.CharField(max_length=50, null=True)
    
## Question-related models.
class QuestionTemplate(models.Model):
    text = models.TextField()
    title = models.CharField(max_length=50)
    
    added_on = models.DateTimeField(auto_now_add=True)
    solver_name = models.CharField(max_length=40)
    
    live = models.BooleanField()

QUESTION_STATUS = (
    ('solved', 'Solved'),       # question has been released and answered
    ('released', 'Released'),   # question has been released but not answered
    ('ready', 'Ready'),         # question parsed and answers available, not released
    ('pending', 'Pending')      # question parsed but answers not available
)
    
class QuestionTag(models.Model):
    name = models.CharField(max_length=100)

class Question(models.Model):
    template = models.ForeignKey(QuestionTemplate)
    user = models.ForeignKey(User, null=True)
    
    text = models.TextField()
    variables = models.TextField()
    
    time_computed = models.DateTimeField(auto_now_add=True)
    time_released = models.DateTimeField(null=True)
    
    status = models.CharField(max_length=10, choices=QUESTION_STATUS)
    order = models.IntegerField()
    
    # Record properties of this question.
    categories = models.ManyToManyField(QuestionTag)
    
    def decoded_text(self):
        base_url = 'http://localhost:8000'
            
        pattern = re.compile('\[\[([a-z0-9\/]+)\]\]')
        matches = pattern.search(self.text)
        if matches is None:
            return self.text
        else:
            path = matches.group(0)[2:-2]
            text = self.text.replace(matches.group(0), '<a href="%s/%s">View link</a>' % (base_url, path))
            return text

class Answer(models.Model):
    question = models.ForeignKey(Question)
    correct = models.BooleanField()
    
    value = models.CharField(max_length=100)
    message = models.CharField(max_length=200, null=True)
    
    time_computed = models.DateTimeField(auto_now_add=True)
    
class Guess(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    
    value = models.CharField(max_length=100)
    correct = models.BooleanField()
    time_guessed = models.DateTimeField()
    
class QuestionHint(models.Model):
    template = models.ForeignKey(QuestionTemplate)
    # The person who provided the hint
    src = models.ForeignKey(User)
    text = models.TextField()
    
    def get_hash(self):
        return hashlib.sha1(str(self.id) + self.text).hexdigest()

class QuestionHintRating(models.Model):
    hint = models.ForeignKey(QuestionHint)
    # The person who provided the rating.
    src = models.ForeignKey(User)
    rating = models.BooleanField()

class QuestionSet(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    # Keeps track of the actual user that has reserved the question set.
    reserved_by = models.ForeignKey(User, null=True)
    questions = models.ManyToManyField(Question)

# Add some stuff to the admin interface.
admin.site.register(RegisLeague)
admin.site.register(RegisUser)
admin.site.register(QuestionTemplate)
admin.site.register(Question)
admin.site.register(QuestionHint)
admin.site.register(Answer)
admin.site.register(Guess)

# Social auth handlers.
from social_auth.signals import socialauth_registered
#from social_auth.backends.google import GoogleBackend
from social_auth.backends.facebook import FacebookBackend


#def google_extra_values(sender, user, response, details, **kwargs):
#    return True

# TODO: This currently doesn't work.  Not a big deal for us but would be nice to fix.
def facebook_extra_values(sender, user, response, details, **kwargs):
    user.email = response.get('email')
    return True

#socialauth_registered.connect(google_extra_values, sender=GoogleBackend)
socialauth_registered.connect(facebook_extra_values, sender=FacebookBackend)