# Generated by Django 3.0.11 on 2021-03-22 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20210316_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='loom',
            name='col_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='loom',
            name='row_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
