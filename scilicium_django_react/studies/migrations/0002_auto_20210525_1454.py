# Generated by Django 3.0.11 on 2021-05-25 14:54

from django.db import migrations
import django.utils.timezone
import scilicium_django_react.studies.models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='updated_at',
            field=scilicium_django_react.studies.models.AutoDateTimeField(default=django.utils.timezone.now),
        ),
    ]