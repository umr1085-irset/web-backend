from django.contrib import admin
from .models import Dataset,Loom,sopMeta,biomaterialMeta
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin
# Register your models here.

class bioMaterialAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = [
        (None,               {'fields': ['tissue','species', 'cell', 'dev_stage', 'cell_Line', 'gender', 'bioType']
                             }
        ),
    ]

admin.site.register(Dataset)
admin.site.register(Loom)
admin.site.register(sopMeta)
admin.site.register(biomaterialMeta,bioMaterialAdmin)