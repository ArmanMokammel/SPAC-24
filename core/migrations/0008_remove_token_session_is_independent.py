# Generated by Django 5.1.4 on 2024-12-22 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_registered_participant_unique_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token_session',
            name='is_independent',
        ),
    ]
