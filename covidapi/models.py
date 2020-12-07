from django.db import models

# Create your models here.
class Country(models.Model):
    name = models.CharField(max_length=200, unique = True)
    slug = models.SlugField()
    code = models.CharField(max_length=50, unique=True)

    def __str__(self): 
        return self.name 

class CountryCasesReport(models.Model):
    country = models.ForeignKey(Country, on_delete = models.CASCADE, related_name='country_cases')
    # url_country_name = models.CharField(max_length=200, unique = True, null=True)
    cases = models.IntegerField(null=True)
    active = models.IntegerField(null=True)
    deaths = models.IntegerField(null=True)
    recovered_cases = models.IntegerField(null=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self): 
        return self.country.name 