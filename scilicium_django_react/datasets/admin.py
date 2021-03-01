from django.contrib import admin
from .models import Dataset, Genome, Species
# Register your models here.

admin.site.register(Dataset)
admin.site.register(Genome)
admin.site.register(Species)
