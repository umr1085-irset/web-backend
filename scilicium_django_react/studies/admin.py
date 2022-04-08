from django.contrib import admin
from .models import *
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.

class articleAdmin(admin.ModelAdmin, DynamicArrayMixin):
    fieldsets = [
        (None,               {'fields': ['title','pmid','doid','bioRxiv', 'pmc', 'keyword', 'topics','shorthand','abstract','journal','volume','releaseDate','author']
                             }
        ),
    ]

admin.site.register(Institute)
admin.site.register(Author)
admin.site.register(Article,articleAdmin)
admin.site.register(Project)
admin.site.register(Study)
admin.site.register(Viewer)
admin.site.register(Contributor)