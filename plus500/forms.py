from django import forms
from django.forms import ModelForm
from plus500.models import Plus500, Settings_table, Emails_Sending

class StyleSettings(forms.ModelForm):
    class Meta:
        model = Settings_table
        fields = ('domain_rating','domain_traffic','referringDomains_backlinks_ratio')
        widgets={

        }
