# Generated by Django 4.1.7 on 2023-04-27 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_startup_establishment_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='startup',
            name='establishment_year',
            field=models.DateField(verbose_name='Establishment Year'),
        ),
    ]
