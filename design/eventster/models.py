from django.db import models
from django.contrib.auth.models import User

class conference(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length = 10)
    Agenda = models.CharField(max_length = 300)
    genre = models.CharField(max_length = 15, choices=( ('edu','educational'),('soc','social'),('ent','entertainment'),('bus','bussiness') ))
    location = models.CharField(max_length = 30)
    time = models.DateTimeField('data published')
    owner = models.ForeignKey(User)
    public = models.BooleanField()


class rsvp(models.Model):
    def __unicode__(self):
      return "%s is attending conference : %s " % (self.user.username, self.rsvp.name)
    user = models.ForeignKey(User)
    rsvp = models.ForeignKey(conference)
    remark= models.CharField(max_length = 100, blank=True, null=True,)

# Create your models here.
