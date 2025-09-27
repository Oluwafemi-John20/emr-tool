from django.contrib import admin
from .models import Medication
@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Medication._meta.get_fields() if not field.many_to_many and not field.one_to_many]

