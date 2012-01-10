from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, UserManager
from django.contrib import admin

class RegisLeague(models.Model):
    name = models.CharField(max_length=100)
    date_created = models.DateField()
    owner = models.ForeignKey('RegisUser')
    
    def __str__(self):
        return self.name

class RegisUser(User):
    # This is how you extend the base user class.
    user = models.OneToOneField(User)
    
    league = models.ForeignKey('RegisLeague')
    
class RegisUserForm(ModelForm):
    class Meta:
        model = RegisUser

## Question-related models.
class QuestionTemplate(models.Model):
    q_text = models.TextField()
    q_title = models.CharField(max_length=50)
    
    added_on = models.TimeField(auto_now_add=True)
    solver_name = models.CharField(max_length=40)

QUESTION_STATUS = (
    ('solved', 'Solved'),
    ('released', 'Released'),
    ('unreleased', 'Unreleased')
)

class Question(models.Model):
    tid = models.ForeignKey(QuestionTemplate)
    uid = models.ForeignKey(RegisUser)
    
    text = models.TextField()
    time_computed = models.TimeField()
    time_released = models.TimeField()
    
    status = models.CharField(max_length=10, choices=QUESTION_STATUS)
    
class Answer(models.Model):
    qid = models.ForeignKey(Question)
    correct = models.BooleanField()
    
    value = models.CharField(max_length=100)
    message = models.CharField(max_length=200)
    
    time_computed = models.TimeField()
    
class Guess(models.Model):
    uid = models.ForeignKey(RegisUser)
    qid = models.ForeignKey(Question)
    
    value = models.CharField(max_length=100)
    time_guessed = models.TimeField()
    
    
# Add some stuff to the admin interface.
admin.site.register(QuestionTemplate)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Guess)