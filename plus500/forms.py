from django import forms
from django.forms import ModelForm
from plus500.models import Plus500, Settings_table

# Create your forms here.

class ContactForm(forms.Form):
    to_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True, initial=Settings_table.objects.get(id__exact=1).email_template)
