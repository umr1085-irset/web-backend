# Generated by Django 3.0.11 on 2020-12-28 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_color',
            field=models.CharField(blank=True, max_length=255, verbose_name='Favorite Color'),
        ),
    ]
