import json, requests

import django
from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError
from covidapi.models import Country, CountryCasesReport

django.setup()


def join_country_name(name):
    lower_name = name.lower()
    return '-'.join(lower_name.split())

def populate_country_cases():
    print("\npopulating countries...\n")
    countries = Country.objects.values('pk','name', 'code')
    total_active = 0
    total_cases = 0
    total_deaths =0
    total_recovered = 0

    for country in countries:
        country_name = join_country_name(country['name'])
        print(country_name)
        response = requests.get('https://api.covid19api.com/total/country/'+country_name)
        if response.status_code == 404:
            continue
        
        if not len(response.json()):
            continue

        last_udpated = response.json()[-1]
        country_instance = Country.objects.get(pk = country['pk'])
        instance, created = CountryCasesReport.objects.get_or_create(country = country_instance)
        
        cache.set(country['code']+ '_confirmed', last_udpated["Confirmed"], 60*60*25)
        cache.set(country['code']+ '_active', last_udpated["Active"], 60*60*25)
        cache.set(country['code']+ '_deaths', last_udpated["Deaths"], 60*60*25)        
        cache.set(country['code']+ '_recovered_cases', last_udpated["Recovered"], 60*60*25)
        
        instance.cases = last_udpated["Confirmed"]
        instance.active = last_udpated["Active"]
        instance.deaths = last_udpated["Deaths"]
        instance.recovered_cases =last_udpated["Recovered"]

        total_cases += last_udpated["Confirmed"]
        total_active += last_udpated["Active"]
        total_deaths += last_udpated["Deaths"]
        total_recovered += last_udpated["Recovered"]


        instance.save()
    cache.set('total_cases', total_cases, 60*60*25)
    cache.set('total_active', total_active, 60*60*25)
    cache.set('total_deaths', total_deaths, 60*60*25)
    cache.set('total_recovered', total_recovered, 60*60*25)
    print("Done")


class Command(BaseCommand):
    help = "loads the countries data into the models"

    def handle(self, *args, **options):
        print("\npopulating countries date in database...")
        populate_country_cases()