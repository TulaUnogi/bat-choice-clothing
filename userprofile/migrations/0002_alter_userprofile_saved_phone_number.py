# Generated by Django 3.2.23 on 2024-04-23 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='saved_phone_number',
            field=models.CharField(blank=True, max_length=17, null=True),
        ),
    ]
