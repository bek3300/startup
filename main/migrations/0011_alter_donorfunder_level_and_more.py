# Generated by Django 4.1.7 on 2023-05-11 05:42

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_incubatorsaccelatorshub_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donorfunder',
            name='level',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), default=list, size=20, verbose_name='Level'),
        ),
        migrations.AlterField(
            model_name='incubatorsaccelatorshub',
            name='ownership',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public'), ('NGO', 'NGO'), ('Government', 'Government'), ('Other', 'Other')], max_length=50, verbose_name='Owner Ship'),
        ),
        migrations.AlterField(
            model_name='incubatorsaccelatorshub',
            name='program_duration',
            field=models.CharField(blank=True, choices=[('less_than_3_month', 'less than 3 month'), ('3_to_6_months', '3 to 6 months'), ('6_months_to_a_year', '6 months to a year'), ('1_year_to_two_years', '1 year to two years'), ('International', 'International')], max_length=50, null=True, verbose_name='Program Duration'),
        ),
    ]