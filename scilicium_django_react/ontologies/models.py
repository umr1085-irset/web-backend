from django.db import models

class Species(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Organ(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Tissue(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class CellLine(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class DevStage(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Pathology(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Chemical(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Omics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Sequencing(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Granularity(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class ExperimentalProcess(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Keyword(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()

class Topics(models.Model):
    ontologyLabel = models.CharField(max_length=200,blank=True, null=True)
    ontologyID = models.CharField(max_length=200,blank=True, null=True)
    displayLabel = models.CharField(max_length=200,blank=True, null=True)
    description =  models.TextField("Description", blank=True, default="")
    as_parent =  models.ManyToManyField("self", related_name='as_children', blank=True) #all parents

    def __str__(self):
        return self.ontologyLabel.capitalize()