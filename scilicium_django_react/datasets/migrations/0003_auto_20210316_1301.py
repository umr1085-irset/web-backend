# Generated by Django 3.0.11 on 2021-03-16 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0002_loom_genenumber'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='loom',
        ),
        migrations.AddField(
            model_name='dataset',
            name='loom',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='as_loom', to='datasets.Loom'),
        ),
    ]
