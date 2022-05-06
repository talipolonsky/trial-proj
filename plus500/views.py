from django.shortcuts import render
from plus500.models import Plus500
import requests
from django.views.generic import CreateView
from .forms import HomeForm

# Create your views here.
def data_updated(request):
    all_links = Plus500.objects.all()
    return render(request, 'refpages/refpage.html', { "all_links":
    all_links} )


def get_home_form(request):
    if request.method == "post":
        home_form = HomeForm(request.POST)
    else:
        home_form = HomeForm()
    return render(request, 'refpages/refpage.html', {'home_form':home_form})
