from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail_sizes', 'original_file_link', 'expiring_link', 'expiring_link_duration']
    list_editable = ['thumbnail_sizes', 'original_file_link', 'exp']


admin.site.register(models.Category)