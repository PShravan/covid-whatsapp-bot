# Generated by Django 3.1.4 on 2020-12-06 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covidapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countrycasesreport',
            name='active',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='countrycasesreport',
            name='cases',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='countrycasesreport',
            name='deaths',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='countrycasesreport',
            name='recovered_cases',
            field=models.IntegerField(null=True),
        ),
    ]
