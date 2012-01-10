from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context

import models.Users

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
  return render_to_response('index.tpl')

def create_account(request):
  form = models.Users.RegisUserForm()
  
  return render_to_response('register.tpl', { 'form' : form })
  
def store_account(request):
  form = models.Users.RegisUserForm(request.POST)
  
  if form.is_valid():
    form.save()
     
  return render_to_response('register.tpl')