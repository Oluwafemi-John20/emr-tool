from django.db import models
from django.utils import timezone
from organizations.models import Organization

GENDER_CHOICES = [
    ("male", "Male"), ("female", "Female"), ("other", "Other"), ("unknown", "Unknown"),
]

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# ---- Patient (FHIR: Patient) ----
class Patient(TimeStampedModel):
    identifiers = models.JSONField(default=list, blank=True, help_text='{system:"MRN", value:"12345"}')  # e.g., [{system:"MRN", value:"12345"}]
    name = models.JSONField(default=dict, blank=True, help_text="FHIR HumanName format: {'family': 'Doe', 'given': ['John']}")         # HumanName
    telecom = models.JSONField(default=list, blank=True, help_text = "Enter list of contacts e.g. [{'system': 'phone', 'value': '+234...'}]")      # phones/emails
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="unknown")
    birthDate = models.DateField(null=True, blank=True, help_text="YYYY-MM-DD")
    address = models.JSONField(default=dict, blank=True, help_text="""{
                                                                        "use": "home", 
                                                                        "type": "physical",
                                                                        "line": ["123 Main Street", "Apt 4B"],
                                                                        "city": "Lagos",
                                                                        "district": "Ikeja",
                                                                        "state": "Lagos State",
                                                                        "postalCode": "100271",
                                                                        "country": "Nigeria"
                                                                        }
                                                                        """)      # Address
    contact = models.JSONField(default=list, blank=True)      # [{relationship(CodeableConcept), name, telecom}]
    managingOrganization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    # created_at = models.DateTimeField(default=timezone.now, editable=False)


    def display_name(self):
        fam = self.name.get("family") if isinstance(self.name, dict) else None
        given = " ".join(self.name.get("given", [])) if isinstance(self.name, dict) else ""
        return (given + " " + (fam or "")).strip() or f"Patient/{self.id}"

    def fhir_reference(self):
        return {"reference": f"Patient/{self.id}", "display": self.display_name()}

    def __str__(self):
        return self.display_name()
