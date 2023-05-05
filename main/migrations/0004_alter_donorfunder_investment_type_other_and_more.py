# Generated by Django 4.1.7 on 2023-05-05 06:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_incubatorsaccelatorshub_focusindustry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donorfunder',
            name='investment_type_other',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='donorfunder',
            name='level',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), default=list, size=20),
        ),
    ]
