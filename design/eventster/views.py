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
from django.contrib.auth.models import User
import json

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
    GET = request.GET
    if('username' in GET and 'password' in GET ):
      lst = []
      user = GET['username']
      paswd = GET['password']
      user = authenticate(username = user , password = paswd)
      if user is not None:
        if user.is_active:
          login(request, user)
          #return HttpResponse('Success')
          return HttpResponse('Success')
        else:
          pass
          #Return a 'disabled account' error message
      else:
        return HttpResponse('Invalid info!')
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
      # adding filter to sort by genre and location
      if('city' in GET and 'genre' in GET):
      	confall = conference.objects.filter(genre__iexact=GET['genre'],location__iexact=GET['city'])
      elif('city' in GET):	 	
      	confall = conference.objects.filter(location__iexact=GET['city'])
      elif('genre' in GET):	 	
      	confall = conference.objects.filter(genre__iexact=GET['genre'])
      elif('query' in GET and GET['query'] in ('genre')):
	#List of genres
	genre_list=['educational','social','entertainment','bussiness']
	return HttpResponse(json.dumps(genre_list))
      elif('query' in GET and GET['query'] in ('user')):
	#List of current registered users, need to change this later
	user_list = []
	for user in User.objects.all():
		user_list.append(user.username)
	return HttpResponse(json.dumps(user_list))
      data = serializers.serialize(GET['output'], (confall if isinstance(confall, Iterable) else [confall]))
      return HttpResponse(data, mimetype='application/' + GET['output'])
    elif('dev' in GET and GET['dev'] in ('and')):
	# Need to change the following if conference model is updated.
	#try:
	con = conference(name=GET['xyz'], Agenda=GET['cba'], genre=GET['nmo'], location=GET['rst'], time=GET['igh'], owner=User.objects.get(username=GET['edf']), private=False if GET['ft']=='False' else True)
	con.save()
	#except:
	#	pass
      	#	#return HttpResponse('error!!')
	return HttpResponse('Conference <b>'+str(con.name)+'</b> Created!!')		
    else:
      return HttpResponse(t.render(c))

