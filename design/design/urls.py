from django.conf.urls import patterns, include, url
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
    url(r'^.*/success', direct_to_template, {'template' : 'eventster/success.html'}),
    url(r'^createconf/', CreateView.as_view(model = conference, success_url = 'success')),
    url(r'^register/', CreateView.as_view(model = User , success_url = 'success')),
    url(r'^login_page/', 'eventster.views.LoginPage'),
    url(r'^conf/$', 'eventster.views.ListConf'),
    url(r'^conf/(?P<conf_id>\d+)/', 'eventster.views.ConfDetail'),
    #url(r'^list_conf/', ListView.as_view(model = conference)),
    # url(r'^design/', include('design.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
