# Generated by Django 4.1.7 on 2023-05-15 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_rename_message_to_messages_from_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='connect',
            name='from_user',
        ),
        migrations.RemoveField(
            model_name='connect',
            name='to_user',
        ),
        migrations.AddField(
            model_name='connect',
            name='requester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='connect',
            name='responser',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='responser', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
