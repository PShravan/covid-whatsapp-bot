from django.urls import include, path
from .views import CountryListView, country_covid_detail, twilio_web_hook

urlpatterns = [
    path('countries/', CountryListView.as_view(), name='country-list'),
    path('country/<str:code>/', country_covid_detail, name='country-report'),
    path('twilio/webhook/', twilio_web_hook, name='twilio_web_hook')
]