from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from scilicium_django_react.ontologies.models import *

class OntoAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['ontologyLabel', 'ontologyID', 'displayLabel', 'description','as_parent']}),
    ]
    list_display = ['ontologyLabel', 'ontologyID']
    search_fields = ['ontologyLabel', 'ontologyID']

admin.site.register(Species, OntoAdmin)
admin.site.register(Organ, OntoAdmin)
admin.site.register(CellLine, OntoAdmin)
admin.site.register(DevStage, OntoAdmin)
admin.site.register(Pathology, OntoAdmin)
admin.site.register(Chemical, OntoAdmin)
admin.site.register(Omics, OntoAdmin)
admin.site.register(Sequencing, OntoAdmin)
admin.site.register(Granularity, OntoAdmin)
admin.site.register(ExperimentalProcess, OntoAdmin)
admin.site.register(Keyword, OntoAdmin)
admin.site.register(Topics, OntoAdmin)
admin.site.register(Tissue, OntoAdmin)