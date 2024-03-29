# Generated by Django 3.0.11 on 2022-01-12 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0008_merge_20220112_0727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='study',
            old_name='project',
            new_name='collection',
        ),
        migrations.RemoveField(
            model_name='study',
            name='scope',
        ),
        migrations.AddField(
            model_name='study',
            name='dataCurators',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='study',
            name='externalID',
            field=models.TextField(blank=True, null=True, verbose_name='externalIDs'),
        ),
        migrations.AddField(
            model_name='study',
            name='viewer',
            field=models.ManyToManyField(blank=True, null=True, related_name='as_study', to='studies.Viewer'),
        ),
        migrations.AlterField(
            model_name='study',
            name='article',
            field=models.ManyToManyField(blank=True, null=True, related_name='study_from', to='studies.Article'),
        ),
        migrations.AlterField(
            model_name='study',
            name='contributor',
            field=models.ManyToManyField(blank=True, null=True, related_name='as_study', to='studies.Contributor'),
        ),
        migrations.AlterField(
            model_name='study',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
    ]
