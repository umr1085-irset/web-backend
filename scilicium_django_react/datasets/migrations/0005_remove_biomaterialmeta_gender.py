# Generated by Django 3.0.11 on 2021-05-25 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0004_auto_20210322_1610'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biomaterialmeta',
            name='gender',
        ),
    ]
