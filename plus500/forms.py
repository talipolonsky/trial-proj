from django import forms

class HomeForm(forms.Form):
    num_of_links = forms.IntegerField(label="Enter # of links")
