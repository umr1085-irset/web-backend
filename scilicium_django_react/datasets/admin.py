from django.contrib import admin
from .models import Dataset,Loom,sopMeta,biomaterialMeta
# Register your models here.

admin.site.register(Dataset)
admin.site.register(Loom)
admin.site.register(sopMeta)
admin.site.register(biomaterialMeta)