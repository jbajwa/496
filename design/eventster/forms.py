from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CreateConfForm(forms.Form):
    name = forms.CharField(max_length = 50)
    Agenda = forms.CharField(max_length = 500)
    genre = forms.CharField(max_length = 15)
    location = forms.CharField(max_length = 40)
    time = forms.DateTimeField('Date/Time')
    private = forms.BooleanField()

class UserForm(UserCreationForm):
    email = forms.EmailField(label = "email")
    class Meta:
      model = User
      fields = ("username", "email")
