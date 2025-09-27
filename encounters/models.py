from django.db import models
from patients.models import Patient
from authenticator.models import TimeStampedModel, Practitioner
from organizations.models import Organization

ENCOUNTER_STATUS = [
    ("planned", "planned"), ("in-progress", "in-progress"),
    ("onleave", "onleave"), ("finished", "finished"), ("cancelled", "cancelled"),
]

ENCOUNTER_CLASS = [
    ("AMB", "Ambulatory"), ("IMP", "Inpatient"), ("EMER", "Emergency"),
    ("VR", "Virtual"), ("HH", "Home Health"),
]

class Encounter(TimeStampedModel):
    status = models.CharField(max_length=20, choices=ENCOUNTER_STATUS, default="in-progress")
    klass = models.CharField("class", max_length=10, choices=ENCOUNTER_CLASS, default="AMB")
    type = models.JSONField(default=list, blank=True)    # [CodeableConcept] e.g., "General medical examination"
    subject = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="encounters")
    serviceProvider = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)
    participant_practitioner = models.ForeignKey(Practitioner, on_delete=models.SET_NULL, null=True, blank=True)
    period = models.JSONField(default=dict, blank=True)  # {"start": iso, "end": iso}
    reasonCode = models.JSONField(default=list, blank=True)  # [CodeableConcept]
    note = models.TextField(blank=True)

    def fhir_reference(self):
        return {"reference": f"Encounter/{self.id}"}

    def __str__(self):
        return f"Encounter/{self.id} - {self.subject}"