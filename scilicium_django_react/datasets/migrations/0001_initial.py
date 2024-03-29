# Generated by Django 3.0.11 on 2021-03-11 09:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_better_admin_arrayfield.models.fields
import scilicium_django_react.datasets.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('studies', '0001_initial'),
        ('ontologies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='biomaterialMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('MIXED', 'Mixed'), ('OTHER', 'Other')], default='MALE', max_length=100)),
                ('bioType', models.CharField(choices=[('ORGAN', 'Organ'), ('TISSUE', 'Tissue'), ('CELL', 'Cell')], default='ORGAN', max_length=100)),
                ('cell', models.ManyToManyField(blank=True, related_name='as_cell', to='ontologies.Cell')),
                ('cell_Line', models.ManyToManyField(blank=True, related_name='as_cellLine', to='ontologies.CellLine')),
                ('dev_stage', models.ManyToManyField(blank=True, related_name='as_dev_stage', to='ontologies.DevStage')),
                ('species', models.ManyToManyField(blank=True, related_name='as_species', to='ontologies.Species')),
                ('tissue', models.ManyToManyField(blank=True, related_name='as_tissue', to='ontologies.Tissue')),
            ],
        ),
        migrations.CreateModel(
            name='sopMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('omics', models.CharField(choices=[('GENOMICS', 'Genomics'), ('TRANSCRIPTOMICS', 'Transcriptomics'), ('EPIGENOMICS', 'Epigenomics'), ('REGULOMICS', 'Regulomics'), ('PROTEOMICS', 'Proteomics'), ('MULTIOMICS', 'Multiomics'), ('OTHER', 'Other')], default='TRANSCRIPTOMICS', max_length=100)),
                ('technoGrain', models.CharField(choices=[('BULK', 'Bulk'), ('SINGLECELL', 'Single Cell'), ('SINGLE NUCLEUS', 'Single Nucleus'), ('SORTEDCELL', 'Sorted cells')], default='BULK', max_length=100)),
                ('technology', models.CharField(choices=[('RNA-SEQ', 'RNA-seq'), ('ATAC-SEQ', 'ATAC-seq'), ('SMART-SEQ', 'SMART-seq'), ('BISULFITE-SEQ', 'Bisulfite-seq'), ('RRBS', 'RRBS'), ('CAGE', 'CAGE'), ('CAP-SEQ', 'CAP-seq'), ('CHIP-SEQ', 'ChIP-seq'), ('DNASE-HYPERSNSITIVITY', 'DNase-Hypersensitivity'), ('HI-C', 'Hi-C'), ('HITS-CLIP', 'HITS-CLIP'), ('HMEDIP-SEQ', 'hMeDIP-seq'), ('MEDIP-SEQ', 'MeDIP-seq'), ('MICROWELL-SEQ', 'Microwell-seq'), ('MIRNA-SEQ', 'miRNA-seq'), ('MNASE-SEQ', 'MNase-seq'), ('MRE-SEQ', 'MRE-seq'), ('NOME-SEQ', 'NOMe-seq'), ('PAS-SEQ', 'PAS-seq'), ('POLYA-SEQ', 'PolyA-seq'), ('SMALLRNA-SEQ', 'smallRNA-seq'), ('TAB-SEQ', 'TAB-seq'), ('WGS', 'WGS')], default='RNA-SEQ', max_length=100)),
                ('expProcess', models.CharField(choices=[('EXPOSURE', 'Exposure'), ('INVESTIGATION', 'Investigation'), ('TREATMENT', 'Treatment')], default='EXPOSURE', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Loom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('loomId', models.CharField(max_length=200, unique=True)),
                ('rowEntity', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), default=list, size=None)),
                ('colEntity', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), default=list, size=None)),
                ('cellNumber', models.IntegerField(blank=True, null=True)),
                ('classes', django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), default=list, size=None)),
                ('file', models.FileField(blank=True, null=True, upload_to=scilicium_django_react.datasets.models.get_upload_path)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loom_upload_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('datasetId', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(choices=[('PENDING', 'Pending approval'), ('PUBLIC', 'Public'), ('PRIVATE', 'Private'), ('RESTRICTED', 'Restricted')], default='PRIVATE', max_length=50)),
                ('bioMeta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dataset_biometa', to='datasets.biomaterialMeta')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='data_upload_created_by', to=settings.AUTH_USER_MODEL)),
                ('loom', models.ManyToManyField(blank=True, related_name='as_loom', to='datasets.Loom')),
                ('sop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dataset_sop', to='datasets.sopMeta')),
                ('study', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dataset_of', to='studies.Study')),
            ],
        ),
    ]
