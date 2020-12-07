from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import render, redirect

from rest_framework import generics
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_xml.renderers import XMLRenderer
from twilio.twiml.messaging_response import MessagingResponse

from .models import Country, CountryCasesReport
from .serializers import CountrySerializer, CountryCasesReportSerializer
# Create your views here.

def home(request):
    return redirect('country-list')

class CountryListView(generics.ListAPIView):
    '''countries list from https://api.covid19api.com/countrie'''
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    # renderer_classes = [XMLRenderer]


@api_view(['POST'])
@renderer_classes([XMLRenderer])
def twilio_web_hook(request):
    '''
        webhook attached in twilio, receives message and sends results of queried country
        searches in cache else queries the database
    '''
    if request.method == 'POST':
        # retrieve incoming message from POST request
        incoming_msg = request.POST['Body'].split()


        if incoming_msg[0] == 'CASES':
            # if cases in message
            if incoming_msg[1] == 'TOTAL':
                # if total in message, then retrieve from cache or database
                if 'total_active' in cache:
                    result = cache.get('total_active')

                else:
                    try:
                        result = CountryCasesReport.objects.aggregate(Sum('active'))
                        if result:
                            cache.set('total_active', result)
                    except:
                        result = 'no country found'

            else:
                # if country code in message, then retrieve from cache or database
                country_code = incoming_msg[1]
                if country_code+'_active' in cache:
                    result = cache.get(country_code+'_active')
                else:
                    try:
                        result =CountryCasesReport.objects.get(country__code=country_code).active
                        if result:
                            cache.set(country_code+'_active', result)
                    except:
                        result = 'no country found'


        if incoming_msg[0] == 'DEATHS':
            #if death in message, then retrieve from cache or database
            if incoming_msg[1] == 'TOTAL':
                #if total in message
                if 'total_deaths' in cache:
                    result = cache.get('total_deaths')

                else:
                    try:
                        result = CountryCasesReport.objects.aggregate(Sum('deaths'))
                        if result:
                            cache.set('total_deaths', result)
                    except:
                        result = 'no country found'

            else:
                country_code = incoming_msg[1]
                if country_code+'_deaths' in cache:
                    result = cache.get(country_code+'_deaths')

                else:
                    # if country code in message, then retrieve from cache or database
                    try:
                        result =CountryCasesReport.objects.get(country__code=country_code).deaths
                        if result:
                            cache.set(country_code+'_deaths', result)
                    except:
                        result = 'no country found'
        else:
            result = 'not found'

        resp = MessagingResponse()
        msg = resp.message()
        msg.body(result)
    return Response(result)


@api_view(['GET'])
def country_covid_detail(request, code):
    # covid details of country queried
    if request.method == 'GET':
        try: 
            country = CountryCasesReport.objects.get(country__code=code)
        except Country.DoesNotExist: 
            return Response({'message': 'Country does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
        country_serializer = CountryCasesReportSerializer(country)
        return Response(country_serializer.data)