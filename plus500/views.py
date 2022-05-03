from django.shortcuts import render
from plus500.models import Plus500
import requests
from django.views.generic import CreateView
from .forms import HomeForm

# Create your views here.
def get_data(request):
    all_links = {}
    url ='https://apiv2.ahrefs.com?from=backlinks&target=ahrefs.com&mode=domain&order_by=ahrefs_rank%3Adesc&select=url_from,ahrefs_rank,domain_rating&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
    try:
        response = requests.get(url)
        data = response.json()
        links = data['refpages']
    except:
        print("Failed reading the data")
    for i in links:
        link_data = Plus500(
            url_from = i['url_from'],
            ahrefs_rank = i['ahrefs_rank'],
            domain_rating = i['domain_rating']
        )
        link_data.save()
        all_links = Plus500.objects.all()

    return render (request, 'refpages/refpage.html', { "all_links":
    all_links} )

def get_home_form(request):
    if request.method == "post":
        home_form = HomeForm(request.POST)
    else:
        home_form = HomeForm()
    return render(request, 'refpages/refpage.html', {'home_form':home_form})
