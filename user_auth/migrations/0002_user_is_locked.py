# Generated by Django 4.2.2 on 2023-07-27 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]