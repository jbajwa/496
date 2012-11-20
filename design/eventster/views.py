from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, render
from django import forms , template
from eventster.models import conference, rsvp
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import serializers
from collections import Iterable

def index(request):
    return render_to_response('eventster/index.html')

def about(request):
    return render_to_response('eventster/about.html')

def LoginPage(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
      if user.is_active:
        login(request, user)
        return render_to_response('eventster/success.html')
      else:
        pass
        #Return a 'disabled account' error message
    else:
      return HttpResponse('Invalid info')
      #Return an 'invalid login' error message.
  else:
    form = UserCreationForm()
    # use render instead of render_to_response
    return render(request, "eventster/login.html", {'form': form,})

def ListConf(request):
    confall = conference.objects.all() 
    t =loader.get_template('eventster/confall.html')
    c = Context({
        'confall': confall,
        })
    return OutputFormat(request,confall,t,c)
    
def ConfDetail(request, conf_id):
    confdetail = conference.objects.get(id=conf_id) 
    t =loader.get_template('eventster/confdetail.html')
    c = Context({
        'confdetail': confdetail,
        })
    # in [] as serializers need iterable as parameter
    return OutputFormat(request,confdetail,t,c)

# Decide to output Json or HTML based on output variable from httprequest
def OutputFormat(request, confall,t,c):
    GET = request.GET
    if('output' in GET and GET['output'] in ('json', 'xml')):
      data = serializers.serialize(GET['output'], (confall if isinstance(confall, Iterable) else [confall]))
      return HttpResponse(data, mimetype='application/' + GET['output'])
    else:
      return HttpResponse(t.render(c))

