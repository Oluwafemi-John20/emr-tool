from django.contrib import admin
from .models import Condition

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Condition._meta.get_fields() if not field.many_to_many and not field.one_to_many]
