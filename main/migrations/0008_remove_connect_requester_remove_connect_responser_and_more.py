# Generated by Django 4.1.7 on 2023-05-15 17:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_remove_connect_from_user_remove_connect_to_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connect',
            name='requester',
        ),
        migrations.RemoveField(
            model_name='connect',
            name='responser',
        ),
        migrations.AddField(
            model_name='connect',
            name='requester',
            field=models.ManyToManyField(related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='connect',
            name='responser',
            field=models.ManyToManyField(related_name='responser', to=settings.AUTH_USER_MODEL),
        ),
    ]