from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, UserManager
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
    
class RegisUserForm(ModelForm):
    class Meta:
        model = RegisUser

REGIS_EVENT_TYPE = (
    ('login', 'Log In'),
)

class RegisEvent(models.Model):
    event_type = models.CharField(max_length=10, choices=REGIS_EVENT_TYPE)
    
    who = models.ForeignKey(RegisUser)
    when = models.DateTimeField(auto_now_add=True)
    
    target = models.CharField(max_length=50, null=True)
    
## Question-related models.
class QuestionTemplate(models.Model):
    q_text = models.TextField()
    q_title = models.CharField(max_length=50)
    
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
    # TODO: Rename this to 'template'
    tid = models.ForeignKey(QuestionTemplate)
    # TODO: Rename this to 'user'
    uid = models.ForeignKey(RegisUser)
    
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
    qid = models.ForeignKey(Question)
    correct = models.BooleanField()
    
    value = models.CharField(max_length=100)
    message = models.CharField(max_length=200, null=True)
    
    time_computed = models.DateTimeField(auto_now_add=True)
    
class Guess(models.Model):
    uid = models.ForeignKey(RegisUser)
    qid = models.ForeignKey(Question)
    
    value = models.CharField(max_length=100)
    correct = models.BooleanField()
    time_guessed = models.DateTimeField()
    
class QuestionHint(models.Model):
    template = models.ForeignKey(QuestionTemplate)
    # The person who provided the hint
    src = models.ForeignKey(RegisUser)
    text = models.TextField()
    
    def get_hash(self):
        return hashlib.sha1(str(self.id) + self.text).hexdigest()

class QuestionHintRating(models.Model):
    hint = models.ForeignKey(QuestionHint)
    # The person who provided the rating.
    src = models.ForeignKey(RegisUser)
    rating = models.BooleanField()

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
from social_auth.backends.google import GoogleBackend

def google_extra_values(sender, user, response, details, **kwargs):
    print 'Updating username'
    user.username = '%s %s' % (response.get('first_name'), response.get('last_name'))
    return True

socialauth_registered.connect(google_extra_values, sender=GoogleBackend)