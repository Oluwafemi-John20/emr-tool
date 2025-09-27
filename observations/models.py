# observations/models.py
from django.db import models
from patients.models import Patient
from encounters.models import Encounter
from organizations.models import Organization
from authenticator.models import User

class Observation(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('preliminary', 'Preliminary'),
        ('final', 'Final'),
        ('amended', 'Amended'),
    ]
    

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="observations")
    encounter = models.ForeignKey(Encounter, on_delete=models.SET_NULL, null=True, blank=True, related_name="observations")
    performer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="performed_observations")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="observations")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    code = models.CharField(max_length=100)  # e.g. "Blood Pressure"
    value = models.CharField(max_length=100) # e.g. "120/80 mmHg"
    unit = models.CharField(max_length=20, blank=True, null=True)  # e.g. "mmHg"
    effective_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.value} {self.unit or ''} for {self.patient}"

