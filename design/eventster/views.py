from django.http import HttpResponse
from django.template import loader, Context
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response, render
from django import forms , template
from eventster.models import conference, rsvp
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core import serializers
from collections import Iterable
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
import json
from forms import CreateConfForm, UserForm
from django.views.decorators.csrf import csrf_exempt

#ERROR/SUCCESS status codes for andriod
STATUS_SUCCESS = 121
STATUS_INVALID_DATE = 221
STATUS_INVALID_PARAM = 222
STATUS_INVALID_USER = 223

def index(request):
    return render(request, 'eventster/index.html', {'user': request.user})

# User.objects.get(id=request.session['member_id']) if ('member_id' in request.session) else None ,})

def about(request):
    return render(request, 'eventster/about.html', {'user': request.user})

def success(request):
    return render(request, 'eventster/success.html', {'user': request.user})

@csrf_exempt
def LoginPage(request):
  if request.method == 'POST':
    if 'android' in request.POST:
	    username = request.POST['username']
	    password = request.POST['password']
 	    #csrf_token =  request.POST['csrf_token']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	      if user.is_active:
		login(request, user)
	        return HttpResponse(STATUS_SUCCESS)
	      else:
		pass
		#Return a 'disabled account' error message
	    else:
	      return HttpResponse(STATUS_INVALID_USER)
	      #Return an 'invalid login' error message.
    else:
	    username = request.POST['username']
	    password = request.POST['password']
	    user = authenticate(username=username, password=password)
	    if user is not None:
	      if user.is_active:
		login(request, user)
		if 'forward' in request.session:
			forward = request.session['forward']
			return render(request, 'eventster/login_success.html', {'user': request.user, 'forward': forward})
		return render(request, 'eventster/login_success.html', {'user': request.user})
	      else:
		pass
		#Return a 'disabled account' error message
	    else:
	      return render(request, 'eventster/login_failure.html', {'user': request.user})
	      #Return an 'invalid login' error message.
	
  else:
    # The following should be removed as we dont do csrf check from android app.
    # Couldnt figure how to add csrf token to the cookie on android side. Hence added csrf_except decorator.
    GET = request.GET
    if('output' in GET ):
	    tkn = get_token(request)
	    return HttpResponse(json.dumps(tkn))
    else:
       form = UserCreationForm()
       if('forward' in GET):
       		request.session['forward']= GET['forward']
       # use render instead of render_to_response
       return render(request, "eventster/login.html", {'form': form, 'user': request.user})

def LogoutAndroid(request):
	GET = request.GET
	if('dev' in GET and GET['dev'] in ('and')):
		#return current user
		if request.user.is_active == False:
			return HttpResponse(STATUS_INVALID_USER)
		logout(request)
		return HttpResponse(STATUS_SUCCESS)
	else:
		return HttpResponse(STATUS_INVALID_PARAM)
	

@csrf_exempt
def CreateConf(request):
  if request.method == 'POST':
    # Populate event using POST protocol
    if 'android' in request.method:
	    POST = request.POST
	    try:
		    con = conference(name=POST['name'], Agenda=POST['Agenda'], genre=POST['genre'], location=POST['location'], date=POST['date'], time=POST['time'], owner=request.user, private=False if 'private' not in POST else True)
		    con.save()
	    except:
	    	    return HttpResponse(STATUS_INVALID_PARAM)
	    return HttpResponse(STATUS_SUCCESS)
    else:	
	    POST = request.POST
	    con = conference(name=POST['name'], Agenda=POST['Agenda'], genre=POST['genre'], location=POST['location'], date=POST['date'], time=POST['time'], owner=request.user, private=False if 'private' not in POST else True)
	    con.save()
	    return render(request, 'eventster/success.html', {'user': request.user})
  
  # Populate event using GET protocol
  if request.method == 'GET':
        GET = request.GET	
	if('dev' in GET and GET['dev'] in ('and')):
	# Need to change the following if conference model is updated.
		try:
			con = conference(name=GET['xyz'], Agenda=GET['cba'], genre=GET['nmo'], location=GET['rst'], date= GET['igh'], time=GET['rss'], owner=request.user, private=False if GET['ft']=='False' else True)
			con.save()
		except:
			if not request.user.is_authenticated():
				return HttpResponse(STATUS_INVALID_USER)
			return HttpResponse(STATUS_INVALID_PARAM)
		return HttpResponse(STATUS_SUCCESS)
	else:
	    form = CreateConfForm()
	    return render(request, "eventster/conference_form.html", {'form': form, 'user': request.user})

@csrf_exempt
def CreateUser(request):
  if request.method == 'POST':
    # save form, creates user with post variables
	if 'android' in request.method:
	    form = userform(request.post)
	    if form.is_valid():
		usr = form.save();
	        usr.backend='django.contrib.auth.backends.modelbackend' 
	        login(request, usr)
		return HttpResponse(STATUS_SUCCESS)
	    return HttpResponse(STATUS_INVALID_PARAM)
		
	else:    
	    form = userform(request.post)
	    if form.is_valid():
	      usr = form.save()
	      # mocking what autheticate does
	      usr.backend='django.contrib.auth.backends.modelbackend' 
	      login(request, usr)
	      if 'forward' in request.session:
		forward = request.session['forward']
		return render(request, 'eventster/login_success.html', {'user': request.user, 'forward': forward})
	      return render(request, 'eventster/login_success.html', {'user': request.user})
  else:
    form = UserForm()

  return render(request, "eventster/register_form.html", {'form': form, 'user': request.user})

def ListConf(request):
    GET = request.GET
    if('events' in GET and GET['events'] in ('myconf')):
   	confall = conference.objects.filter(owner=request.user)
    else:
    	confall = conference.objects.all() 
    t =loader.get_template('eventster/confall.html')
    c = Context({
        'confall': confall, 'user': request.user,
        })
    return OutputFormat(request,confall,t,c)
    
def ConfDetail(request, conf_id):
    confdetail = conference.objects.get(id=conf_id) 
    rsvpobjs = None
    if 'output' in request.GET:
	    t =loader.get_template('eventster/confdetail.html')
	    c = Context({
		'confdetail': confdetail, 'user': request.user,
		})
	    # in [] as serializers need iterable as parameter
	    return OutputFormat(request,confdetail,t,c)
    else:
	    rlist = []
            for rs in rsvp.objects.filter(rsvp=confdetail):
		rlist.append(rs.user.username)
	    t =loader.get_template('eventster/confdetail.html')
	    c = Context({
		'confdetail': confdetail, 'user': request.user, 'rsvpobjs': rsvpobjs , 'rsvplist': rlist,
		})
    return HttpResponse(t.render(c))

def Rsvp(request):
    GET = request.GET
    conf = conference.objects.get(id=GET['confid'])
    rsvpobjs = None
    # dev = device , and = android, when RSVP from android properly return correct httpresponse
    if ('acc' in GET and GET['acc'] in ('add')):
	    if ('dev' in GET and GET['dev'] in ('and')) and request.user.is_authenticated() == False :
		return HttpResponse(STATUS_INVALID_USER)
	    r = rsvp(user = request.user, rsvp = conf, remark='none')
	    r.save()
	    if ('dev' in GET and GET['dev'] in ('and')):
		return HttpResponse(STATUS_SUCCESS)

    elif ('acc' in GET and GET['acc'] in ('remove')):
	    if ('dev' in GET and GET['dev'] in ('and')) and request.user.is_authenticated() == False :
		return HttpResponse(STATUS_INVALID_USER)
	    r = rsvp.objects.get(user = request.user, rsvp = conf)
	    r.delete()
	    if ('dev' in GET and GET['dev'] in ('and')):
		return HttpResponse(STATUS_SUCCESS)
    elif ('event' in GET and GET['event'] in ('attendees')):
	    rsvpobjs = rsvp.objects.filter(rsvp=conf)
    rlist = []
    userlist = []
    for rs in rsvp.objects.filter(rsvp=conf):
	rlist.append(rs.user.username)
	userlist.append(rs.user)
    # Return to Android the list of user attending the conference
    t =loader.get_template('eventster/confdetail.html')
    c = Context({
	'confdetail': conf, 'user': request.user, 'rsvpobjs': rsvpobjs , 'rsvplist': rlist,
        })
    return OutputFormat(request, userlist , t, c)
    

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
	genre_list=['educational','social','entertainment','business']
	return HttpResponse(json.dumps(genre_list))
      elif('query' in GET and GET['query'] in ('user')):
	#List of current registered users, need to change this later
	user_list = []
	for user in User.objects.all():
		user_list.append(user.username)
	return HttpResponse(json.dumps(user_list))
      elif('query' in GET and GET['query'] in ('currentuser')):
	#return current user
	user = request.user.username
	if request.user.is_active == False:
		return HttpResponse(STATUS_INVALID_USER)
	return HttpResponse(json.dumps(user))
      elif('query' in GET and GET['query'] in ('myconf')):
	if request.user.is_active == True:
      		confall = conference.objects.filter(owner=request.user)
	else:
		return HttpResponse(STATUS_INVALID_USER)
      data = serializers.serialize(GET['output'], (confall if isinstance(confall, Iterable) else [confall]))
      return HttpResponse(data, mimetype='application/' + GET['output'])
    else:
      return HttpResponse(t.render(c))

