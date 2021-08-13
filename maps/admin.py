from django.contrib import admin
from .models import MapGeometry, CompletedMaps, FinalMaps, ApprovedMap

admin.site.register(MapGeometry)
admin.site.register(CompletedMaps)
admin.site.register(FinalMaps)
admin.site.register(ApprovedMap)
