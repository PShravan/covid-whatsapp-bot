# Generated by Django 3.1.4 on 2020-12-07 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covidapi', '0002_auto_20201206_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycasesreport',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_cases', to='covidapi.country'),
        ),
    ]
