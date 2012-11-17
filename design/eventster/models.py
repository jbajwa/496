from django.db import models
from django.contrib.auth.models import User

class conference(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length = 10)
    Agenda = models.CharField(max_length = 300)
    genre = models.CharField(max_length = 15)
    location = models.CharField(max_length = 30)
    time = models.DateTimeField('data published')
    owner = models.ForeignKey(User)


class rsvp(models.Model):
    user = models.ForeignKey(User)
    rsvp = models.ForeignKey(conference)
    remark= models.CharField(max_length = 100)

# Create your models here.
