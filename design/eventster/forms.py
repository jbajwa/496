from django import forms

class CreateConfForm(forms.Form):
    name = forms.CharField(max_length = 50)
    Agenda = forms.CharField(max_length = 500)
    genre = forms.CharField(max_length = 15)
    location = forms.CharField(max_length = 40)
    time = forms.DateTimeField('Date/Time')
    private = forms.BooleanField()
