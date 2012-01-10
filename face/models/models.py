from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User, UserManager

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