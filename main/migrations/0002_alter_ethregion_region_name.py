# Generated by Django 4.1.7 on 2023-04-23 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ethregion',
            name='region_name',
            field=models.CharField(choices=[('Addis Ababa', 'Addis Ababa'), ('Afar', 'Afar'), ('Amhara', 'Amhara'), ('Benishangul-Gumuz', 'Benishangul-Gumuz'), ('Dire Dawa', 'Dire Dawa'), ('Gambela', 'Gambela'), ('Harari', 'Harari'), ('Oromia', 'Oromia'), ('Somali', 'Somali'), ('Sidama', 'Sidama '), ('South West Peoples', 'South West'), ('SNNP', 'SNNP'), ('Tigray', 'Tigray')], max_length=50, unique=True),
        ),
    ]