from django.contrib import admin
from .models import Dataset, Genome, Species, Study, DataType, VisualisationReader, VisualizationType
# Register your models here.

admin.site.register(Dataset)
admin.site.register(Genome)
admin.site.register(Species)
admin.site.register(Study)
admin.site.register(DataType)
admin.site.register(VisualizationType)
admin.site.register(VisualisationReader)