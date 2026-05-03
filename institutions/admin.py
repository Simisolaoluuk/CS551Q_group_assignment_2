from django.contrib import admin
from .models import Region, Institution, PerformanceRecord

admin.site.register(Region)
admin.site.register(Institution)
admin.site.register(PerformanceRecord)
