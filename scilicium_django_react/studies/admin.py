from django.contrib import admin
from .models import *
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

# Register your models here.

admin.site.register(Institute)
admin.site.register(Author)
admin.site.register(Article)
admin.site.register(Project)
admin.site.register(Study)