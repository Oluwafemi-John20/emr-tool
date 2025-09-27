from django.contrib import admin
from .models import User, Practitioner

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in User._meta.get_fields() if not field.many_to_many and not field.one_to_many]
    # search_fields = ("Username", "id")

@admin.register(Practitioner)
class PractitionerAdmin(admin.ModelAdmin):
    list_display = list_display = [field.name for field in Practitioner._meta.get_fields() if not field.many_to_many and not field.one_to_many]