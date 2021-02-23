from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField

# Create your models here.
from django.contrib.auth.models import  User
from scilicium_django_react.projects.models import Project
from django.utils.text import slugify

class VisualisationReader(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class VisualizationType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField( blank=True, null=True)
    reader = models.ManyToManyField(VisualisationReader, related_name='as_reader',blank=True)

    def __str__(self):
        return self.name

class DataType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField( blank=True, null=True)

    def __str__(self):
        return self.name


class Species(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField( blank=True, null=True)

    def __str__(self):
        return self.name

class Genome(models.Model):
    version = models.CharField(max_length=200,unique=True)
    species = models.ForeignKey(Species, on_delete=models.CASCADE, related_name='version_of')
    description = models.TextField()

    def __str__(self):
        return self.version

class Dataset(models.Model):
    DATA_STATUS = (
        ('PENDING', 'Pending approval'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('RESTRICTED', 'Restricted'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField()
    genome = models.ForeignKey(Genome, on_delete=models.CASCADE, related_name='from_genome_version', blank=True, null=True)
    data_type = models.ForeignKey(DataType,on_delete=models.CASCADE, related_name='data_as_type', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='data_upload_created_by')
    upload = models.FileField(upload_to='datasets/%Y/%m/%d/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=DATA_STATUS, default="PRIVATE")
    display_types = models.ManyToManyField(VisualizationType, related_name='display_as', blank=True)
    default_display = models.ForeignKey(VisualizationType, blank=True, null=True, on_delete=models.SET_NULL, related_name='default_display_as')
    config_page = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name

class Study(models.Model):

    DATASET_STATUS = (
        ('PENDING', 'Pending approval'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('RESTRICTED', 'Restricted'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField()
    description = models.TextField("description", blank=True)
    author = models.CharField(max_length=200, blank=True)
    publication = models.IntegerField(blank=True, null=True)
    pmid = models.CharField(max_length=200, blank=True)
    data = models.ManyToManyField(Dataset, related_name='in_dataset',blank=True)
    status = models.CharField(max_length=50, choices=DATASET_STATUS, default="PRIVATE")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='dataset_created_by')
    

    def __str__(self):
        return self.title