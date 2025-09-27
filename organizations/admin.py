from django.contrib import admin
from .models import Organization

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Organization._meta.get_fields() if not field.many_to_many and not field.one_to_many]
