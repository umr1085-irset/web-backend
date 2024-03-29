# Generated by Django 3.0.11 on 2022-09-22 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontologies', '0002_auto_20210617_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='BiomaterialType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ontologyLabel', models.CharField(blank=True, max_length=200, null=True)),
                ('ontologyID', models.CharField(blank=True, max_length=200, null=True)),
                ('displayLabel', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('as_parent', models.ManyToManyField(blank=True, related_name='_biomaterialtype_as_parent_+', to='ontologies.BiomaterialType')),
            ],
        ),
    ]
