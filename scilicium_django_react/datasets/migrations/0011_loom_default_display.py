# Generated by Django 3.0.11 on 2021-06-28 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0010_auto_20210622_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='loom',
            name='default_display',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]