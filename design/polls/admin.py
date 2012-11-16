from polls.models import Choice
from django.contrib import admin

class PollAdmin(admin.ModelAdmin):
        pass
        #fields = ['pub_date','question']
admin.site.register(Choice, PollAdmin)
