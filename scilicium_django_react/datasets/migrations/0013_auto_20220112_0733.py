# Generated by Django 3.0.11 on 2022-01-12 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0010_auto_20220112_0733'),
        ('datasets', '0012_auto_20220112_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='contributor',
            field=models.ManyToManyField(blank=True, related_name='contributor_dataset', to='studies.Contributor'),
        ),
    ]