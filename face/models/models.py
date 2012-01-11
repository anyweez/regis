from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, UserManager
from django.contrib import admin

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


## Question-related models.
class QuestionTemplate(models.Model):
    q_text = models.TextField()
    q_title = models.CharField(max_length=50)
    
    added_on = models.DateTimeField(auto_now_add=True)
    solver_name = models.CharField(max_length=40)

QUESTION_STATUS = (
    ('solved', 'Solved'),       # question has been released and answered
    ('released', 'Released'),   # question has been released but not answered
    ('ready', 'Ready'),         # question parsed and answers available, not released
    ('pending', 'Pending')      # question parsed but answers not available
)

class Question(models.Model):
    tid = models.ForeignKey(QuestionTemplate)
    uid = models.ForeignKey(User)
    
    text = models.TextField()
    variables = models.TextField()
    
    time_computed = models.DateTimeField(auto_now_add=True)
    time_released = models.DateTimeField(null=True)
    
    status = models.CharField(max_length=10, choices=QUESTION_STATUS)
    order = models.IntegerField()
    
class Answer(models.Model):
    qid = models.ForeignKey(Question)
    correct = models.BooleanField()
    
    value = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    
    time_computed = models.DateTimeField(auto_now_add=True)
    
class Guess(models.Model):
    uid = models.ForeignKey(User)
    qid = models.ForeignKey(Question)
    
    value = models.CharField(max_length=100)
    correct = models.BooleanField()
    time_guessed = models.DateTimeField()
    
    
# Add some stuff to the admin interface.
admin.site.register(RegisLeague)
admin.site.register(RegisUser)
admin.site.register(QuestionTemplate)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Guess)