from django.shortcuts import render
from plus500.models import Plus500
import requests
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F #for the django queries

@login_required
def home(request):
    all_links = Plus500.objects.all()[:10]
    return render(request, 'plus500/home.html', {'all_links': all_links})

@login_required
def home_after_filter(request):
    num_of_links= int(request.GET.get('links_num'))
    all_categories = {"news": request.GET.get('news'),
        "finance": request.GET.get('finance'),"crypto": request.GET.get('crypto'),
        "forex": request.GET.get('forex'),"commodities": request.GET.get('commodities'),
        "leisure": request.GET.get('leisure')}
    selected_categories = []
    #for category, bool_category in all_categories.items():
    #    if bool_category:
    #        selected_categories.append[category]
    #for selected_category in selected_categories:
    #    all_links = Plus500.objects.get(category=selected_category)
    #num1 = 70
    #all_links = Plus500.objects.filter(domain_rating=F('num1'))[:num_of_links]
    all_links = Plus500.objects.all()[:num_of_links]
    return render(request, 'plus500/home.html', {'all_links': all_links})

@login_required
def settings(request):
    return render(request, 'plus500/settings.html')
