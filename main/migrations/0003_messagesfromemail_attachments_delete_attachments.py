# Generated by Django 5.0.6 on 2024-07-02 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_messagesfromemail_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagesfromemail',
            name='attachments',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.DeleteModel(
            name='Attachments',
        ),
    ]
