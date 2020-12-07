from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render

from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse

from .models import Country, CountryCasesReport
from .serializers import CountrySerializer, CountryCasesReportSerializer
# Create your views here.

class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


@api_view(['POST'])
def hook_twilio_message(request):
    user_id = request.POST.get('id', None)
    # Save the payment status
    payment = Payment.objects.get(user_id=user_id)
    payment.payment_successful = True
    payment.save()
    return HttpResponse('success')

@api_view(['POST'])
def twilio_web_hook(request):
    if request.method == 'POST':
        # retrieve incoming message from POST request in lowercase
        incoming_msg = request.POST['Body'].split()
        if incoming_msg[0] == 'CASES':
            if incoming_msg[1] == 'TOTAL':
                result = cache.get('total_active')
                if not result:
                    result = CountryCasesReport.objects.aggregate(Sum('active'))
            else:
                country_code = incoming_msg[1]
                if country_code+'_active' in cache:
                    result = cache.get(country_code+'_active')
                else:
                    result = CountryCasesReportSerializer.objects.get(country__code=country_code).active

        if incoming_msg[0] == 'DEATHS':
            if incoming_msg[1] == 'TOTAL':
                if 'total_deaths' in cache:
                    result = cache.get('total_deaths')
                else:
                    try:
                        result = CountryCasesReport.objects.aggregate(Sum('deaths'))
                    except:
                        result = 'no country found'
            else:
                country_code = incoming_msg[1]
                if country_code+'_active' in cache:
                    result = cache.get(country_code+'_active')
                else:
                    try:
                        result =CountryCasesReportSerializer.objects.get(country__code=country_code).deaths
                    except:
                        result = 'no country found'
        
        else:
            result = 'not found'


        # create Twilio XML response
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(result)
        if Country.objects.get(code = incoming_msg):
            response = "*Hi! I am the Quarantine Bot*"
            msg.body(response)
        else:
            x= incoming_msg:
    return Response(result)




@api_view(['GET'])
def country_covid_detail(request, code):
    try: 
        country = Country.objects.get(code=code) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 

class CountryCasesView(APIView):
    def get(self, request, format=None):
        request.get()
        return Response(usernames)