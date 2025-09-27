from django.contrib import admin
from .models import Observation

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Observation._meta.get_fields() if not field.many_to_many and not field.one_to_many]
