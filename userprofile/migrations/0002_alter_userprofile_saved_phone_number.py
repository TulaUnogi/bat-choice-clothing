# Generated by Django 3.2.23 on 2024-06-30 20:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='saved_phone_number',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+123456789'.                     Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]