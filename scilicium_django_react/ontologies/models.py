from django.db import models

class Species(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Organ(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Tissue(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class CellLine(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class DevStage(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class BiomaterialType(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Pathology(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Chemical(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Omics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Sequencing(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Granularity(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class ExperimentalProcess(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Keyword(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel

class Topics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.displayLabel
