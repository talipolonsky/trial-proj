from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model, login, \
                                logout, authenticate


def home(request):
    return render(request, 'main/home.html')
# Create your views here.
