# Generated by Django 4.1.7 on 2023-05-03 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_remove_mentor_educationallevel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mentor',
            name='attachments',
            field=models.FileField(blank=True, help_text='please upload relevant documents max 10', null=True, upload_to='mentor/attachments', verbose_name='Attachment'),
        ),
    ]
