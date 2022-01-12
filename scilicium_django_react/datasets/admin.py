from django.contrib import admin
from .models import Dataset,Loom,sopMeta,biomaterialMeta
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
# Register your models here.

class bioMaterialAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = [
        (None,               {'fields': ['biomaterialCollectedFrom','tissue','organ','species', 'developmentStage', 'sex', 'biomaterialType','age_start','age_end','age_unit','diseaseStage']
                             }
        ),
    ]

class datasetAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = [
        (None,               {'fields': ['title','datasetId','autoNbID','description', 'created_by','keywords','loom','status','study','sop','bioMeta']
                             }
        ),
    ]

admin.site.register(Dataset,datasetAdmin)
admin.site.register(Loom)
admin.site.register(sopMeta)
admin.site.register(biomaterialMeta,bioMaterialAdmin)