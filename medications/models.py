from django.db import models
from authenticator.models import TimeStampedModel, Practitioner
from django.utils import timezone
from patients.models import Patient
from encounters.models import Encounter

MEDREQ_STATUS = [
    ("active", "active"), ("on-hold", "on-hold"), ("cancelled", "cancelled"),
    ("completed", "completed"), ("entered-in-error", "entered-in-error"),
    ("stopped", "stopped"), ("draft", "draft"),
]

MEDREQ_INTENT = [
    ("proposal", "proposal"), ("plan", "plan"), ("order", "order"),
    ("original-order", "original-order"), ("reflex-order", "reflex-order"),
    ("filler-order", "filler-order"), ("instance-order", "instance-order"),
    ("option", "option"),
]

class Medication(TimeStampedModel):
    code = models.JSONField(default=dict)   # CodeableConcept (RxNorm/WHO ATC/local)
    status = models.CharField(max_length=20, default="active")  # free text ok MVP
    form = models.JSONField(default=dict, blank=True)  # CodeableConcept e.g., tablet
    manufacturer = models.CharField(max_length=255, blank=True)

    def fhir_reference(self):
        return {"reference": f"Medication/{self.id}", "display": self.code.get("text")}

    def __str__(self):
        return self.code.get("text") or f"Medication/{self.id}"

class MedicationRequest(TimeStampedModel):
    status = models.CharField(max_length=20, choices=MEDREQ_STATUS, default="active")
    intent = models.CharField(max_length=30, choices=MEDREQ_INTENT, default="order")
    medication = models.ForeignKey(Medication, on_delete=models.SET_NULL, null=True, blank=True)
    medicationText = models.CharField(max_length=255, blank=True)  # fallback if no FK
    subject = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="medication_requests")
    encounter = models.ForeignKey(Encounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="medication_requests")
    requester = models.ForeignKey(Practitioner, on_delete=models.SET_NULL, null=True, blank=True)
    authoredOn = models.DateTimeField(default=timezone.now)
    dosageInstruction = models.JSONField(default=list, blank=True)  # [ {text | timing | doseAndRate{doseQuantity{value,unit}}} ]
    dispenseRequest = models.JSONField(default=dict, blank=True)    # {validityPeriod, quantity, expectedSupplyDuration}

    def fhir_reference(self):
        return {"reference": f"MedicationRequest/{self.id}"}

    def __str__(self):
        return self.medicationText or (self.medication and self.medication.__str__()) or f"MedicationRequest/{self.id}"