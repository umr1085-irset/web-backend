from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import  User, Group
from django.conf import settings

class Species(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Organ(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Tissue(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class CellLine(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class DevStage(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Pathology(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Chemical(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Omics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Sequencing(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Granularity(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class ExperimentalProcess(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Keyword(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()

class Topics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.name.capitalize()