# Generated by Django 4.1.7 on 2023-05-10 09:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_incubatorsaccelatorshub_focusindustry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incubatorsaccelatorshub',
            name='level',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), default=list, size=20, verbose_name='Level'),
        ),
    ]