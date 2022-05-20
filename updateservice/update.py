import subprocess, sys
from django.shortcuts import render
from plus500.models import Plus500
import requests
from urllib.parse import urlparse

def traffic_for_url(url_from):
    domain = urlparse(url_from).netloc
    domain = 'ahrefs.com'
    traffic_url = 'https://apiv2.ahrefs.com?from=positions_metrics&target=' + domain + '&mode=subdomains&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
    traffic_response = requests.get(traffic_url)
    traffic_data = traffic_response.json()
    traffics = traffic_data['metrics']
    traffic = traffics['traffic']
    return traffic

def refdomain_for_url(url_from):
    domain = urlparse(url_from).netloc
    domain = 'ahrefs.com'
    refdomain_url = 'https://apiv2.ahrefs.com?from=refdomains_by_type&target=' + domain + '&mode=subdomains&limit=1&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
    refdomain_response = requests.get(refdomain_url)
    refdomain_data = refdomain_response.json()
    all_refdomains = refdomain_data['stats']
    refdomain =all_refdomains['refdomains']
    return refdomain



def get_data():
    all_links = {}
    Plus500.objects.all().delete()
    target_list=['ahrefs.com']
    for target in target_list:
        url = 'https://apiv2.ahrefs.com?from=backlinks&target=' + target + '&mode=subdomains&limit=50&order_by=ahrefs_rank%3Adesc&select=url_from,ahrefs_rank,domain_rating,url_to,title&output=json&token=082c4afc97f7348b730e5fc0b861a2ebd9ce522a'
        try:
            response = requests.get(url)
            data = response.json()
            links = data['refpages']
        except:
            print("Failed reading the data")
        url_from_list = []
        for i in links:
            url_from_1 = i['url_from']
            url_from_list.append(url_from_1)
            link_data = Plus500(
                url_from = i['url_from'],
                url_to = i['url_to'],
                ahrefs_rank = i['ahrefs_rank'],
                domain_rating = i['domain_rating'],
                title = i['title'],
                competitor = target
            )
            link_data.save()
        for url in url_from_list:
            refdomain_value=refdomain_for_url(url)
            Plus500.objects.filter(url_from=url,competitor=target).update(refdomains=refdomain_value)
            traffic_value=traffic_for_url(url)
            Plus500.objects.filter(url_from=url,competitor=target).update(traffic=traffic_value)
    all_links = Plus500.objects.all()
    return (all_links)
