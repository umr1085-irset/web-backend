from django.db import models
from django.conf import settings
from django.utils import timezone 
# Create your models here.
from django.contrib.auth.models import  User


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()

class Institute(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):

    fullName = models.CharField(max_length=200)
    affiliation = models.ManyToManyField(Institute, related_name='author_from', blank=True)

    def __str__(self):
        return self.fullName

class Article(models.Model):

    title = models.CharField(max_length=200)
    pmid = models.CharField(max_length=200, blank=True, null=True)
    abstract = models.TextField("description", blank=True)
    journal = models.CharField(max_length=200, blank=True, null=True)
    volume = models.IntegerField(blank=True, null=True)
    releaseDate = models.DateTimeField(auto_now=False, null=True)
    author = models.ManyToManyField(Author, related_name='write_by', blank=True)

    def __str__(self):
        return self.title


class Project(models.Model):

    PROJECT_STATUS = (
        ('PENDING', 'Pending approval'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('RESTRICTED', 'Restricted'),
    )

    title = models.CharField(max_length=200)
    projectId = models.CharField(max_length=200)
    description = models.TextField("description", blank=True)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS, default="PRIVATE")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='project_created_by')

    def __str__(self):
        return self.title
    
    # Override save method to auto increment project custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Project, self).save(*args, **kwargs)
        self.projectId = "hup" + str(self.id)
        super(Project, self).save()


class Study(models.Model):

    STUDY_STATUS = (
        ('PENDING', 'Pending approval'),
        ('PUBLIC', 'Public'),
        ('PRIVATE', 'Private'),
        ('RESTRICTED', 'Restricted'),
    )
    
    STUDY_TOPICS = (
        ('GONAD DEVELOPMENT', 'Gonad development'),
        ('OTHER', 'Other'),
    )

    title = models.CharField(max_length=200)
    studyId = models.SlugField(max_length=200)
    description = models.TextField("description", blank=True)
    status = models.CharField(max_length=50, choices=STUDY_STATUS, default="PRIVATE")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='study_created_by')
    updated_at = AutoDateTimeField(default=timezone.now)
    topics = models.CharField(max_length=100, choices=STUDY_TOPICS, default="PRIVATE")
    project = models.ForeignKey(Project, blank=True, null=True, on_delete=models.SET_NULL, related_name='study_of')
    article = models.ManyToManyField(Article, related_name='study_from', blank=True)

    def __str__(self):
        return self.title

    # Override save method to auto increment study custom id
    def save(self, *args, **kwargs):
        force = kwargs.pop('force', False)
        super(Study, self).save(*args, **kwargs)
        self.studyId = "hus" + str(self.id)
        super(Study, self).save()
