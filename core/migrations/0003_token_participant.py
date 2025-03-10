# Generated by Django 5.1.4 on 2024-12-15 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_token_session_order_of_session'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token_Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('registered_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.registered_participant')),
                ('token_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.token_session')),
            ],
            options={
                'verbose_name': 'Applied Participant Token',
            },
        ),
    ]
