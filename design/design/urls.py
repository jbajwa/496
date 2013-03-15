from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.simple import direct_to_template
from eventster.models import conference
from django.contrib.auth.models import User
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
#generic view
from django.views.generic import DetailView, CreateView, ListView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'design.views.index', name='home'),
    #url(r'^$', direct_to_template, {'template' : 'index.html'}),
    url(r'^$', 'eventster.views.index'),
    url(r'^about/$', 'eventster.views.about'),
    url(r'^.*/success', 'eventster.views.success'),
    url(r'^createconf/', 'eventster.views.CreateConf'),
    url(r'^register/', 'eventster.views.CreateUser'),
    url(r'^rsvp/', 'eventster.views.Rsvp'),
    # commented django-register for now, need to setup stmp server for that
    # url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^login_page/', 'eventster.views.LoginPage'),
    url(r'^logout/', 'django.contrib.auth.views.logout', {'next_page':'/'}),
    url(r'^logout_android/', 'eventster.views.LogoutAndroid'),
    url(r'^conf/$', 'eventster.views.ListConf'),
    url(r'^conf/(?P<conf_id>\d+)/', 'eventster.views.ConfDetail'),

    #file upload urls
    # conf/file/...

    url(r'^delete/(\d+)/$', 'eventster.views.FileDel'),
    url(r'^upload/$', 'eventster.views.FileUploader'),

    #url(r'^list_conf/', ListView.as_view(model = conference)),
    # url(r'^design/', include('design.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
