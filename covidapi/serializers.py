from rest_framework import serializers

from .models import Country, CountryCasesReport

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'

class CountryCasesReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCasesReport
        fields = ('country', 'cases', 'deaths', 'status', 'date_updated')