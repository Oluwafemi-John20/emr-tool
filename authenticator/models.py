from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

# core/models.py
from django.conf import settings
from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Role choices
    role = models.CharField(
        max_length=20,
        choices=[
            ("ADMIN", "Admin"),
            ("DOCTOR", "Doctor"),
            ("NURSE", "Nurse"),
            ("PATIENT", "Patient"),
        ],
        default="PATIENT"
    )

    # Link to organization (if you have an Organization model)
    organization = models.ForeignKey(
        "organizations.Organization",  # assuming app name = organization
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    # Email is already included in AbstractUser, but we can enforce uniqueness
    email = models.EmailField(unique=True)

    # first_name and last_name are already in AbstractUser
    
    def __str__(self):
        return f"{self.username} ({self.role})"


# ---- Common Base ----
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Practitioner(TimeStampedModel):
    # NOTE: You can link to Django's auth.User via OneToOne if desired.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="practitioner_profile")
    identifiers = models.JSONField(default=list, blank=True)  # license numbers, etc.
    name = models.JSONField(default=dict, blank=True)         # HumanName {family, given:[], prefix:[]}
    telecom = models.JSONField(default=list, blank=True)      # [{system, value, use}]
    qualification = models.JSONField(default=list, blank=True)# [{identifier, code(CodeableConcept), issuer(Org ref)}]
    active = models.BooleanField(default=True)

    def display_name(self):
        fam = self.name.get("family") if isinstance(self.name, dict) else None
        given = " ".join(self.name.get("given", [])) if isinstance(self.name, dict) else ""
        return (given + " " + (fam or "")).strip() or self.user.get_full_name() or self.user.username

    def fhir_reference(self):
        return {"reference": f"Practitioner/{self.id}", "display": self.display_name()}

    def __str__(self):
        return self.display_name()
