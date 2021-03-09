import os
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField

# Create your models here.
from django.contrib.auth.models import  User
from scilicium_django_react.studies.models import Study
from scilicium_django_react.ontologies.models import CellLine, Cell, Species, Tissue, DevStage
from django.utils.text import slugify


def get_upload_path(instance, filename):

    user_type = "user"
    if instance.created_by and instance.created_by.is_superuser:
        user_type = "admin"

    path =  os.path.join("datasets/loom/{}/{}/".format(user_type, instance.loomId), filename)
    return path
        
class biomaterialMeta(models.Model):
    BIO_TYPE = (
        ('ORGAN','Organ'),
        ('TISSUE','Tissue'),
        ('CELL','Cell'),
    )

    GENDER = (
        ('MALE','Male'),
        ('FEMALE','Female'),
        ('MIXED','Mixed'),
        ('OTHER','Other'),
    )
    tissue = models.ManyToManyField(Tissue, related_name='as_tissue', blank=True)
    species = models.ManyToManyField(Species, related_name='as_species', blank=True)
    cell = models.ManyToManyField(Cell, related_name='as_cell', blank=True)
    dev_stage = models.ManyToManyField(DevStage, related_name='as_dev_stage', blank=True)
    cell_Line = models.ManyToManyField(CellLine, related_name='as_cellLine', blank=True)
    gender = models.CharField(max_length=100, choices=GENDER, default="MALE")
    bioType = models.CharField(max_length=100, choices=BIO_TYPE, default="ORGAN")

    def __str__(self):
        return self.id


class sopMeta(models.Model):
    OMICS_VALUES = (
        ('GENOMICS', 'Genomics'),
        ('TRANSCRIPTOMICS', 'Transcriptomics'),
        ('EPIGENOMICS', 'Epigenomics'),
        ('REGULOMICS', 'Regulomics'),
        ('PROTEOMICS', 'Proteomics'),
        ('MULTIOMICS', 'Multiomics'),
        ('OTHER', 'Other'),
    )

    TECHNO_GRAIN = (
        ('BULK','Bulk'),
        ('SINGLECELL','Single Cell'),
        ('SINGLE NUCLEUS','Single Nucleus'),
        ('SORTEDCELL','Sorted cells'),
    )

    TECHNO = (
        ('RNA-SEQ','RNA-seq'),
        ('ATAC-SEQ','ATAC-seq'),
        ('SMART-SEQ','SMART-seq'),
        ('BISULFITE-SEQ','Bisulfite-seq'),
        ('RRBS','RRBS'),
        ('CAGE','CAGE'),
        ('CAP-SEQ','CAP-seq'),
        ('CHIP-SEQ','ChIP-seq'),
        ('DNASE-HYPERSNSITIVITY','DNase-Hypersensitivity'),
        ('HI-C','Hi-C'),
        ('HITS-CLIP','HITS-CLIP'),
        ('HMEDIP-SEQ','hMeDIP-seq'),
        ('MEDIP-SEQ','MeDIP-seq'),
        ('MICROWELL-SEQ','Microwell-seq'),
        ('MIRNA-SEQ','miRNA-seq'),
        ('MNASE-SEQ','MNase-seq'),
        ('MRE-SEQ','MRE-seq'),
        ('NOME-SEQ','NOMe-seq'),
        ('PAS-SEQ','PAS-seq'),
        ('POLYA-SEQ','PolyA-seq'),
        ('SMALLRNA-SEQ','smallRNA-seq'),
        ('TAB-SEQ','TAB-seq'),
        ('WGS','WGS'),

    )

    EXP_VALUE = (
        ('EXPOSURE','Exposure'),
        ('INVESTIGATION','Investigation'),
        ('TREATMENT','Treatment'),
    )
    omics = models.CharField(max_length=100, choices=OMICS_VALUES, default="TRANSCRIPTOMICS")
    technoGrain = models.CharField(max_length=100, choices=TECHNO_GRAIN, default="BULK")
    technology = models.CharField(max_length=100, choices=TECHNO, default="RNA-SEQ")
    expProcess = models.CharField(max_length=100, choices=EXP_VALUE, default="EXPOSURE")

    def __str__(self):
        return self.id

class Loom(models.Model):
    name = models.CharField(max_length=200,unique=True)
    loomId = models.CharField(max_length=200,unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='loom_upload_created_by')
    rowEntity = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    colEntity = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)

    def __str__(self):
        return self.name

    # Override save method to auto increment loom custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Loom, self).save(*args, **kwargs)
        self.loomId = "hul" + str(self.id)
        super(Loom, self).save()


class Dataset(models.Model):
    DATA_STATUS = (
        ('PENDING', 'Pending approval'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('RESTRICTED', 'Restricted'),
    )

    title = models.CharField(max_length=200)
    datasetId = models.CharField(max_length=200,unique=True)
    description = models.TextField("description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='data_upload_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    loom = models.ManyToManyField(Loom, related_name='as_loom', blank=True)
    status = models.CharField(max_length=50, choices=DATA_STATUS, default="PRIVATE")
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_of')
    sop = models.ForeignKey(sopMeta, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_sop')
    bioMeta = models.ForeignKey(biomaterialMeta, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_biometa')
    

    def __str__(self):
        return self.title
    
    # Override save method to auto increment dataset custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Dataset, self).save(*args, **kwargs)
        self.datasetId = "hud" + str(self.id)
        super(Dataset, self).save()