from django.db import models

class Poll(models.Model):
        def __unicode__(self):
                return self.question
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('data published')

class Choice(models.Model):
    def __unicode__(self):
            return self.choice
    poll  = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
