# Generated by Django 3.0.11 on 2023-04-18 12:50

from django.db import migrations, models
import scilicium_django_react.datasets.models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0015_auto_20220922_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='loom',
            name='light_file',
            field=models.FileField(blank=True, null=True, upload_to=scilicium_django_react.datasets.models.get_upload_path),
        ),
    ]
