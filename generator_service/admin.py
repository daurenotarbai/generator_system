from django.contrib import admin
from .models import *

class SchemaBasicInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblSchemaBasicInfo._meta.fields]

class SchemaColumnsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblSchemaColumns._meta.fields]

class DataSetsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TblDataSets._meta.fields]

admin.site.register(TblSchemaBasicInfo, SchemaBasicInfoAdmin)
admin.site.register(TblSchemaColumns, SchemaColumnsAdmin)
admin.site.register(TblDataSets, DataSetsAdmin)