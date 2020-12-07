import json, requests

import django
from django.core.management.base import BaseCommand, CommandError
from covidapi.models import Country

django.setup()

def populate_countries():
    print("\npopulating countries...\n")
    response = requests.get('https://api.covid19api.com/countries')
    for country in response.json():
        print("adding: ",country['Country'])
        movie_obj = Country.objects.create(name=country['Country'],slug=country['Slug'],code=country['ISO2'])
    print("Done")


class Command(BaseCommand):
    help = "loads the countries data into the models"

    def handle(self, *args, **options):
        print("\npopulating countries date in database...")
        print("\ndeleting all previous data...")
        Country.objects.all().delete()
        print("Deletion Done\n\n")
        populate_countries()