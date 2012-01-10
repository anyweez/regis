from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import Context, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import models.models as users
import errors.errorman as errorman

# View is activated when the index page is viewed.
# There's not a lot of dynamic action here at
# this point.
def index(request):
    return render_to_response('index.tpl', { 'errors' : errorman.get_printable_errors() }, context_instance=RequestContext(request))

def create_account(request):
    form = users.RegisUserForm()
  
    return render_to_response('register.tpl', { 'form' : form })
  
def store_account(request):
    form = users.RegisUserForm(request.POST)
  
    if form.is_valid():
        form.save()
     
    return render_to_response('register.tpl')

@login_required
def dash(request):
    
    return render_to_response('dashboard.tpl', { 'user': request.user })

def login(request):    
    if len(request.POST['username']) > 0 and len(request.POST['password']) > 0:
        uname = request.POST['username']
        pwd = request.POST['password']
        user = auth.authenticate(username=uname, password=pwd)
        
        if user is not None:
            if user.is_active:
                return redirect('/dash')
                # Correct, let's proceed
            else:
                errorman.register_error(3)
                return redirect('/')
                # Correct, but account has been deactivated
        else:
            # Username or password is incorrect.
            errorman.register_error(2)
            return redirect('/')
    else:
        errorman.register_error(1) # Register an error saying info was missing.
        # Didn't provide a username or password.
        return redirect('/')
