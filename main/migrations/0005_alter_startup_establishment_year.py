# Generated by Django 4.1.7 on 2023-04-26 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_profile_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='establishment_year',
            field=models.DateField(verbose_name='By year range'),
        ),
    ]
