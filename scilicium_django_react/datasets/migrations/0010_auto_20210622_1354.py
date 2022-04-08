# Generated by Django 3.0.11 on 2021-06-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ontologies', '0002_auto_20210617_0824'),
        ('datasets', '0009_loom_reducions'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loom',
            old_name='reducions',
            new_name='reductions',
        ),
        migrations.AddField(
            model_name='biomaterialmeta',
            name='age_unit',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='sopmeta',
            name='expProcess',
        ),
        migrations.AddField(
            model_name='sopmeta',
            name='expProcess',
            field=models.ManyToManyField(blank=True, related_name='as_experimental', to='ontologies.ExperimentalProcess'),
        ),
        migrations.RemoveField(
            model_name='sopmeta',
            name='omics',
        ),
        migrations.AddField(
            model_name='sopmeta',
            name='omics',
            field=models.ManyToManyField(blank=True, related_name='as_omics', to='ontologies.Omics'),
        ),
        migrations.RemoveField(
            model_name='sopmeta',
            name='technoGrain',
        ),
        migrations.AddField(
            model_name='sopmeta',
            name='technoGrain',
            field=models.ManyToManyField(blank=True, related_name='as_granularity', to='ontologies.Granularity'),
        ),
        migrations.RemoveField(
            model_name='sopmeta',
            name='technology',
        ),
        migrations.AddField(
            model_name='sopmeta',
            name='technology',
            field=models.ManyToManyField(blank=True, related_name='as_sequencing', to='ontologies.Sequencing'),
        ),
    ]
