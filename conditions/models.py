from django.utils import timezone
from django.db import models
from patients.models import Patient
from authenticator.models import TimeStampedModel, User
from encounters.models import Encounter


CONDITION_CLINICAL_STATUS = [
    ("active", "active"), ("recurrence", "recurrence"), ("relapse", "relapse"),
    ("inactive", "inactive"), ("remission", "remission"), ("resolved", "resolved"),
]

CONDITION_VERIFICATION_STATUS = [
    ("unconfirmed", "unconfirmed"), ("provisional", "provisional"),
    ("differential", "differential"), ("confirmed", "confirmed"),
    ("refuted", "refuted"), ("entered-in-error", "entered-in-error"),
]

class Condition(TimeStampedModel):
    clinicalStatus = models.CharField(max_length=20, choices=CONDITION_CLINICAL_STATUS, default="active")
    verificationStatus = models.CharField(max_length=20, choices=CONDITION_VERIFICATION_STATUS, default="confirmed")
    category = models.JSONField(default=list, blank=True)  # [CodeableConcept], e.g., "encounter-diagnosis"
    code = models.JSONField(default=dict)                  # CodeableConcept with ICD-10/SNOMED coding
    subject = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="conditions")
    encounter = models.ForeignKey(Encounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="conditions")
    onsetDateTime = models.DateTimeField(null=True, blank=True)
    recordedDate = models.DateTimeField(default=timezone.now)
    recorder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def fhir_reference(self):
        return {"reference": f"Condition/{self.id}"}

    def __str__(self):
        text = self.code.get("text") if isinstance(self.code, dict) else None
        return text or f"Condition/{self.id}"
