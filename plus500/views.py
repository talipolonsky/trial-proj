from django.shortcuts import render
from plus500.models import Plus500, Settings_table
import requests
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F #for the django queries
from django.shortcuts import render, redirect
#from django.core.exceptions import ValidationError, SuspiciousOperation

@login_required
def home(request):
    # the dictionary we will return to home.html
    context = {'links_num_exception': False} #flag if there is an exception in the num_links
    #bringing the setting_object for the last saved links_num in settings
    setting_object = Settings_table.objects.get(id__exact=1)
    #bringing all links from the DB and then filter them by category
    selected_links = Plus500.objects.all()

    if request.GET.get('links_num'): #if the submit button has pressed
        #updating the links_num in the settigns table if was tipped number of links:
        #if request.GET.get('selected_num'):
        try:
            num_links= int(request.GET.get('links_num'))
            if num_links >= 0:
                setting_object.links_num = num_links
                setting_object.save()
            else:
                context.update({'links_num_exception': True})
        except:
            context.update({'links_num_exception': True})
        #else:
        #    setting_object.links_num = 100

        #selection of categories:
        all_categories = {"news": request.GET.get('news'),
             "finance": request.GET.get('finance'),"crypto": request.GET.get('crypto'),
             "forex": request.GET.get('forex'),"commodities": request.GET.get('commodities'),
             "leisure": request.GET.get('leisure')}

        unselected_categories = []
        for category, bool_category in all_categories.items():
            if not bool_category:
                unselected_categories.append(category)
        for unselected_category in unselected_categories:
            selected_links = selected_links.exclude(category=unselected_category)
    else:
        setting_object.links_num = 50

    num_of_links= setting_object.links_num
    selected_links = selected_links.filter(domain_rating__gt=setting_object.domain_rating)[:num_of_links]
    #selected_links = selected_links.order_by('-pub_date', 'headline')[:num_of_links]
    #he result above will be ordered by pub_date descending, then by headline ascending. The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied.
    context.update({'selected_links': selected_links, 'num_of_links': num_of_links})

    return render(request, 'plus500/home.html', context)


@login_required
def settings(request):
    #send flags of exceptions:
    context = {'domain_rating_exception': False, 'domain_traffic_exception': False,
     'RB_ratio_exception': False, 'none_exception': False}
    setting_object = Settings_table.objects.get(id__exact=1)
    #updating the fields of the object with id=1:
    if request.method == 'POST':
        if request.POST.get('DR'):
            try:
                setting_object.domain_rating = int(request.POST.get('DR'))
            except:
                context.update({'domain_rating_exception': True})
        if request.POST.get('DT'):
            try:
                setting_object.domain_traffic = int(request.POST.get('DT'))
            except:
                context.update({'domain_traffic_exception': True})
        if request.POST.get('RB_ratio'):
            try:
                setting_object.referringDomains_backlinks_ratio = int(request.POST.get('RB_ratio'))
            except:
                context.update({'RB_ratio_exception': True})

        setting_object.save()

        #for alert of Success:
        none_exception = not context['domain_rating_exception'] and not context['domain_traffic_exception'] and not context['RB_ratio_exception']
        if none_exception:
                context.update({'none_exception': True})

    context.update({'setting_object': setting_object})
    return render(request, 'plus500/settings.html', context)
