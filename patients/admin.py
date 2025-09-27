from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Patient._meta.get_fields() if not field.many_to_many and not field.one_to_many]

