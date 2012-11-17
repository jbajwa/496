from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django import forms
from eventster.models import conference, rsvp
#to create generic form to create object
from django.views.generic.edit import CreateView

def index(request):
    t = loader.get_template('eventster/index.html')
    return HttpResponse(t.render())

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        #Redirect to a success page.
      else:
        pass
        #Return a 'disabled account' error message
    else:
      pass
      #Return an 'invalid login' error message.
  else:
    form = UserCreationForm()
    return render_to_response("eventster/register.html", {'form': form,})

def create_conf(request):
    
    return CreateView()

def list_conf(request):
    confall = conference.objects.all() 
    t =loader.get_template('eventster/confall.html')
    c = Context({
        'confall': confall,
        })
    return HttpResponse(t.render(c))
