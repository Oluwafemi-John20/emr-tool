from django.contrib import admin
from .models import Encounter

@admin.register(Encounter)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Encounter._meta.get_fields() if not field.many_to_many and not field.one_to_many]

