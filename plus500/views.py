from django.shortcuts import render
from plus500.models import Plus500, Settings_table
import requests
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F #for the django queries
from django.shortcuts import render, redirect
from plus500.forms import *
import csv
from django.http import HttpResponse
import datetime
from plus500.forms import ContactForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

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

    # filter on unselected competitors:
    all_competitors = {"avatrae": setting_object.avatrae,
         "robinhood": setting_object.robinhood,"etoro": setting_object.etoro,
         "IG": setting_object.IG,"CMC_markets": setting_object.CMC_markets}

    unselected_competitors = []
    for competitor, bool_competitor in all_competitors.items():
        if not bool_competitor:
            unselected_competitors.append(competitor)
    for unselected_competitor in unselected_competitors:
        selected_links = selected_links.exclude(competitor=unselected_competitor)

    # filter on minimum in each metric:
    selected_links = selected_links.filter(domain_rating__gt=setting_object.domain_rating)

    #sorting by selected priorities:
    #explanation of -: selected_links = selected_links.order_by('-pub_date', 'headline')[:num_of_links]
    #he result above will be ordered by pub_date descending, then by headline ascending. The negative sign in front of "-pub_date" indicates descending order. Ascending order is implied.
    priority_dict = {setting_object.domain_rating_priority: '-domain_rating',
                    setting_object.domain_traffic_priority: 'traffic',
                    setting_object.referringDomains_backlinks_ratio_priority: '-refdomains_backlinks_ratio'}
    #for key in sorted(priority_dict):
    try:
        first_order = priority_dict[0]
        second_order = priority_dict[1]
        third_order = priority_dict[2]
        selected_links = selected_links.order_by(first_order, second_order, third_order)
    except Exception as e: print(e)
    #selected_links = selected_links.order_by('-domain_rating_priority', '-domain_traffic_priority')[:num_of_links]

    selected_links = selected_links[:num_of_links]
    context.update({'selected_links': selected_links, 'num_of_links': num_of_links})

    if 'form-1-submit' in request.POST:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            to_email = form.cleaned_data['to_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, to_email, to_email)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    else:
        form = ContactForm()
        context.update({'form': form})
        
    return render(request, 'plus500/home.html', context)

#@login_required
# Create your views here.
#def homepage(request):
#	return render(request, "main/home.html")

# @login_required
# def contactView(request):
#     if request.method == 'GET':
#         form = ContactForm()
#     else:
#         form = ContactForm(request.POST)
#         if form.is_valid():
#             subject = form.cleaned_data['subject']
#             from_email = form.cleaned_data['from_email']
#             message = form.cleaned_data['message']
#             try:
#                 send_mail(subject, message, from_email, ['admin@example.com'])
#             except BadHeaderError:
#                 return HttpResponse('Invalid header found.')
#             return redirect('success')
#     return render(request, 'plus500/home.html', {'form': form})

@login_required
def settings(request):
    #send flags of exceptions:
    # form = StyleSettings
    # context = {'form': form}
    context = {'domain_rating_exception': False, 'domain_traffic_exception': False, 'RB_ratio_exception': False,
    'priority_range_exception': False, 'email_template_exception': False, 'none_exception': False}

    setting_object = Settings_table.objects.get(id__exact=1)
    #updating the fields of the object with id=1:
    if request.method == 'POST':
        #sorting metrics:
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

        #sorting prioritities:
        try:
            dr = int(request.POST.get('DR_priority'))
            dt = int(request.POST.get('DT_priority'))
            br = int(request.POST.get('RB_ratio_priority'))
            #check if the priority includes all: 0,1,2
            priority_range = (0,1,2)
            for i in priority_range:
                if i not in (dr, dt, br):
                    context.update({'priority_range_exception': True})
                    break
            if not context['priority_range_exception']:
                setting_object.domain_rating_priority = dr
                setting_object.domain_traffic_priority = dt
                setting_object.referringDomains_backlinks_ratio_priority = br
        except:
            context.update({'priority_range_exception': True})

        #competitor companies:
        if request.POST.get('avatrae'):
            setting_object.avatrae = True
        else:
            setting_object.avatrae = False
        if request.POST.get('robinhood'):
            setting_object.robinhood = True
        else:
            setting_object.robinhood = False
        if request.POST.get('etoro'):
            setting_object.etoro = True
        else:
            setting_object.etoro = False
        if request.POST.get('IG'):
            setting_object.IG = True
        else:
            setting_object.IG = False
        if request.POST.get('CMC_markets'):
            setting_object.CMC_markets = True
        else:
            setting_object.CMC_markets = False

        #Email Template:
        try:
            setting_object.email_template = request.POST.get('email_template')
        except:
            context.update({'email_template_exception': True})

        setting_object.save()

        #for alert of Success:
        none_exception = not context['domain_rating_exception'] and not context['domain_traffic_exception'] and not context['RB_ratio_exception'] and not context['email_template_exception'] and not context['priority_range_exception']
        if none_exception:
                context.update({'none_exception': True})

    context.update({'setting_object': setting_object})
    return render(request, 'plus500/settings.html', context)

@login_required
def export_to_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= Daily_Data' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Website where the Backlink is Found','Domain of the Website','The Competitor which the backlink is Pointing to','Competitor Domain','Domain Rating','Refdomains','Traffic','Refdomains/Backlinks Ratio', 'Website Category','Website Contacts Emails'])
    plus500 = Plus500.objects.all()
    for item in plus500:
        writer.writerow([item.url_from, item.url_domain, item.url_to,item.competitor,item.domain_rating,item.refdomains,item.traffic, item.refdomains_backlinks_ratio, item.category, item.contact_email])
    return response
