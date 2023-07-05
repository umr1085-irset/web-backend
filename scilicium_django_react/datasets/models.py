import os
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django_better_admin_arrayfield.models.fields import ArrayField
from django.dispatch import receiver

import os
import shutil

# Create your models here.
from django.contrib.auth.models import  User
from scilicium_django_react.studies.models import Study, Contributor
from scilicium_django_react.ontologies.models import CellLine, Species, Tissue, DevStage, Organ, Chemical, Omics, Granularity, Sequencing, ExperimentalProcess, Pathology, BiomaterialType
from django.utils.text import slugify
from scilicium_django_react.utils.loom_reader import *

def get_upload_path(instance, filename):

    user_type = "user"
    if instance.created_by and instance.created_by.is_superuser:
        user_type = "admin"

    path =  os.path.join("datasets/loom/{}/{}/".format(user_type, instance.id), filename)
    return path
        
class biomaterialMeta(models.Model):
    #BIO_TYPE = (
      #  ('ORGAN','Organ'),
      #  ('TISSUE','Tissue'),
      #  ('CELL','Cell'),
      #  ('BLOOD','Blood'),
      #  ('TUMOR TISSUE', 'Tumor tissue'),
      #  ('NORMAL TISSUE', 'Normal tissue'),
    #)

    GENDER = (
        ('male','Male'),
        ('female','Female'),
        ('mixed','Mixed'),
        ('other','Other'),
        ('unknown','Unknown'),
    )
    name = models.CharField(max_length=100, default="",blank=True, null=True)
    tissue = models.ManyToManyField(Tissue, related_name='as_tissue', blank=True)
    organ = models.ManyToManyField(Organ, related_name='as_organ', blank=True)
    species = models.ManyToManyField(Species, related_name='as_species', blank=True)
    developmentStage = models.ManyToManyField(DevStage, related_name='as_dev_stage', blank=True)
    #cell_Line = models.ManyToManyField(CellLine, related_name='as_cellLine', blank=True)
    sex = ArrayField(models.CharField(max_length=32, blank=True, choices=GENDER),default=list,blank=True)
    #biomaterialType = models.CharField(max_length=100, choices=BIO_TYPE, default="ORGAN")
    biomaterialType = models.ManyToManyField(BiomaterialType, related_name='as_biomaterialType', blank=True)
    age_start = models.IntegerField(blank=True, null=True)
    age_end = models.IntegerField(blank=True, null=True)
    age_unit = models.CharField(max_length=100, default="",blank=True, null=True)
    diseaseStage = models.CharField(max_length=100, default="",blank=True, null=True)
    pathology = models.ManyToManyField(Pathology, related_name='as_pathology', blank=True)

    def __str__(self):
        return self.name

class sopMeta(models.Model):
    name = models.CharField(max_length=100, default="",blank=True, null=True)
    omics = models.ManyToManyField(Omics, related_name='as_omics', blank=True)
    resolution = models.ManyToManyField(Granularity, related_name='as_granularity', blank=True)
    technology = models.ManyToManyField(Sequencing, related_name='as_sequencing', blank=True)
    techno_description = models.TextField("description", blank=True, null=True)
    experimentalDesign = models.ManyToManyField(ExperimentalProcess, related_name='as_experimental', blank=True)
    molecule_applied = models.ManyToManyField(Chemical, related_name='is_exposed', blank=True)
    
    def __str__(self):
        return self.name

class Loom(models.Model):
    name = models.CharField(max_length=200,unique=False)
    loomId = models.CharField(max_length=200,unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='loom_upload_created_by')
    rowEntity = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    colEntity = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    reductions = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    cellNumber =  models.IntegerField(blank=True, null=True)
    geneNumber = models.IntegerField(blank=True, null=True)
    row_name = models.CharField(max_length=200, blank=True, null=True)
    col_name = models.CharField(max_length=200, blank=True, null=True)
    classes = ArrayField(models.CharField(max_length=200, blank=True), default=list)
    file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    light_file = models.FileField(upload_to=get_upload_path, blank=True, null=True)
    default_display = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    # Override save method to auto increment loom custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Loom, self).save(*args, **kwargs)
        if self.file and self.file.name:
            loomattr = extract_attr_keys(self.file.path)
            shape = get_shape(self.file.path)
            self.reductions = get_available_reductions(self.file.path)
            self.rowEntity = loomattr['row_attr_keys']
            self.colEntity = loomattr['col_attr_keys']
            self.classes = get_classes(self.file.path)
            self.cellNumber = shape[1]
            self.geneNumber = shape[0]
        self.loomId = "l" + str(self.id)
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
    autoNbID = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField("description", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='data_upload_created_by')
    updated_at = models.DateTimeField(auto_now=True, null=True)
    keywords = ArrayField(models.CharField(max_length=200, blank=True), default=list, blank=True, null=True)
    loom = models.ForeignKey(Loom, on_delete=models.SET_NULL, null=True, related_name='as_loom', blank=True)
    status = models.CharField(max_length=50, choices=DATA_STATUS, default="PRIVATE")
    study = models.ForeignKey(Study, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_of')
    sop = models.ForeignKey(sopMeta, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_sop')
    bioMeta = models.ForeignKey(biomaterialMeta, blank=True, null=True, on_delete=models.SET_NULL, related_name='dataset_biometa')
    contributor = models.ManyToManyField(Contributor, related_name='contributor_dataset', blank=True)
    

    def __str__(self):
        return self.title
    
    # Override save method to auto increment dataset custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Dataset, self).save(*args, **kwargs)
        self.datasetId = "d" + str(self.id)
        super(Dataset, self).save()

@receiver(models.signals.pre_delete, sender=Dataset)
def auto_delete_loomfile_on_delete(sender, instance, **kwargs):
    # Delete the folder
    local_path = f"{instance.loom.loomId.replace('l','')}"
    unix_path = settings.MEDIA_ROOT + "/datasets/loom/admin/" + local_path
    if(os.path.exists(unix_path)):
       shutil.rmtree(unix_path) # delete loom folder
    Loom.objects.filter(loomId=instance.loom.loomId).delete() # delete Loom entry in Django DB