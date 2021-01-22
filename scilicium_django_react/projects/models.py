from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import  User

class Project(models.Model):

    PROJECT_STATUS = (
        ('PENDING', 'Pending approval'),
        ('WAIT', 'Wait for samples'),
        ('SEQUENCING', 'Sequencing'),
        ('ANALYSIS', 'Analysis'),
        ('DONE', 'Finish'),
        ('ERROR', 'Error'),
        ('ARCHIVED', 'Archived'),
        ('AVAILABLE', 'Data available'),
        ('STOP', 'Stop'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField("description", blank=True)
    status = models.CharField(max_length=50, choices=PROJECT_STATUS, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE, related_name='project_created_by')

    def __str__(self):
        return self.name