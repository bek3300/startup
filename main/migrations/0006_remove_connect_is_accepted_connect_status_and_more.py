# Generated by Django 4.1.7 on 2023-05-06 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_donorfunder_doner_type_by_other_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connect',
            name='is_accepted',
        ),
        migrations.AddField(
            model_name='connect',
            name='status',
            field=models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'Rejected')], default=1),
        ),
        migrations.AlterField(
            model_name='goveroment',
            name='goveroment_type',
            field=models.CharField(choices=[('ministry_offices', 'Ministry offices'), ('universities', 'Universities'), ('Other', 'Other')], max_length=50, verbose_name='Government type'),
        ),
    ]