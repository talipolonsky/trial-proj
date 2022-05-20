from django.shortcuts import render
from plus500.models import Plus500, Settings_table
import requests
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F #for the django queries
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError, SuspiciousOperation

@login_required
def home(request):
    all_links = Plus500.objects.all()[:10]
    return render(request, 'plus500/home.html', {'all_links': all_links})

@login_required
def home_after_filter(request):
    num_of_links= int(request.GET.get('links_num'))

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
    # all_categories = {"news": request.GET.get('news'),
    #     "finance": request.GET.get('finance'),"crypto": request.GET.get('crypto'),
    #     "forex": request.GET.get('forex'),"commodities": request.GET.get('commodities'),
    #     "leisure": request.GET.get('leisure')}
    # form = Settings_table(request.POST or None)
    # if request.method == 'GET':
    #     context = {'Settings_table':Settings_table}
    #     return render(request, 'plus500/settings.html', context)
    #
    # if request.method == 'POST':
    #     if form.is_valid():
    #         form.save()
    #         # handle valid form here. eg:
    #         return render(request, 'plus500/settings.html')
    #         # return redirect('some_view')
    #     else:
    #         # handle invalid form
    #         raise ValidationError('form was invalid')
    # # method was neither "GET" nor "POST", raise a 405: Method Not Allowed
    # raise SuspiciousOperation(405)
    if request.method == 'POST':
        settings_data = Settings_table(
            domain_rating = request.POST.get('DR'),
            domain_traffic = request.POST.get('DT'),
            referringDomains_backlinks_ratio = request.POST.get('RB_ratio'),
            is_news = request.POST.get('news'),
            is_finance = request.POST.get('finance'),
            is_crypto = request.POST.get('crypto'),
            is_forex = request.POST.get('forex'),
            is_commodities = request.POST.get('commodities'),
        )
        settings_data.save()
    settings_profile = Settings_table.objects.latest('id')
    # Update the fields in the Settings_table:
    # Settings_table.domain_rating = request.GET.get('DR')
    # Settings_table.domain_traffic = request.GET.get('DT')
    # Settings_table.referringDomains_backlinks_ratio = request.GET.get('RB_ratio')
    # if request.GET.get('news'):
    #     Settings_table.is_news = True
    # if request.GET.get('finance'):
    #     Settings_table.is_finance = True
    # if request.GET.get('crypto'):
    #     Settings_table.is_crypto = True
    # if request.GET.get('forex'):
    #     Settings_table.is_forex = True
    # if request.GET.get('commodities'):
    #     Settings_table.is_commodities = True
    # settings_profile = {'dr': Settings_table.domain_rating, 'dt': Settings_table.domain_traffic, 'ratio': Settings_table.referringDomains_backlinks_ratio}
    return render(request, 'plus500/settings.html', {'settings_profile': settings_profile})
