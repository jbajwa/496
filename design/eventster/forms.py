from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateConfForm(forms.Form):
    name = forms.CharField(max_length = 50)
    Agenda = forms.CharField(max_length = 500)
    genre = forms.CharField(max_length = 15)
    location = forms.CharField(max_length = 40)
    date = forms.DateField('Date')
    time = forms.TimeField('Time')
    private = forms.BooleanField()

class UserForm(UserCreationForm):
    email = forms.EmailField(label = "email")
    class Meta:
      model = User
      fields = ("first_name", "last_name", "username", "email")
