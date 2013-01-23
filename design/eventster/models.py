from django.db import models
from django.contrib.auth.models import User

class conference(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length = 50)
    Agenda = models.CharField(max_length = 500)
    genre = models.CharField(max_length = 15, choices=( ('educational','educational'),('social','social'),('entertainment','entertainment'),('bussiness','bussiness') ))
    location = models.CharField(max_length = 40)
    date= models.DateField('Date')
    time = models.TimeField('Time')
    owner = models.ForeignKey(User)
    private = models.BooleanField()


class rsvp(models.Model):
    def __unicode__(self):
      return "%s is attending conference : %s " % (self.user.username, self.rsvp.name)
    user = models.ForeignKey(User)
    rsvp = models.ForeignKey(conference)
    remark= models.CharField(max_length = 500, blank=True, null=True,)
    class Meta:
       unique_together = ('user', 'rsvp',)

# Create your models here.
