# Generated by Django 3.0.11 on 2021-02-10 14:24

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('upload', models.FileField(blank=True, null=True, upload_to='datasets/%Y/%m/%d/')),
                ('status', models.CharField(choices=[('PENDING', 'Pending approval'), ('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('RESTRICTED', 'Restricted')], default='PRIVATE', max_length=50)),
                ('config_page', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_upload_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DataType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisualisationReader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='VisualizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('reader', models.ManyToManyField(blank=True, related_name='as_reader', to='datasets.VisualisationReader')),
            ],
        ),
        migrations.CreateModel(
            name='Study',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField()),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('author', models.CharField(blank=True, max_length=200)),
                ('publication', models.IntegerField(blank=True, null=True)),
                ('pmid', models.CharField(blank=True, max_length=200)),
                ('status', models.CharField(choices=[('PENDING', 'Pending approval'), ('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('RESTRICTED', 'Restricted')], default='PRIVATE', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dataset_created_by', to=settings.AUTH_USER_MODEL)),
                ('data', models.ManyToManyField(blank=True, related_name='in_dataset', to='datasets.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='Genome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField()),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='version_of', to='datasets.Species')),
            ],
        ),
        migrations.AddField(
            model_name='dataset',
            name='data_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_as_type', to='datasets.DataType'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='default_display',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='default_display_as', to='datasets.VisualizationType'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='display_types',
            field=models.ManyToManyField(blank=True, related_name='display_as', to='datasets.VisualizationType'),
        ),
        migrations.AddField(
            model_name='dataset',
            name='genome',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_genome_version', to='datasets.Genome'),
        ),
    ]
