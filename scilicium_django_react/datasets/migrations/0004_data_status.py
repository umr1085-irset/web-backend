# Generated by Django 3.0.11 on 2021-01-20 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20210119_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending approval'), ('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('RESTRICTED', 'Restricted')], default='PRIVATE', max_length=50),
        ),
    ]
