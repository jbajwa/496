from django.http import HttpResponse

def index(request):
    t = loader.get_template('conference/index.html')
    return HttpResponse(t.render())

def create_conf(request):
    return HttpResponse("Create conf!")
