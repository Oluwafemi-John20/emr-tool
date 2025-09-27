from django.db import models
from authenticator.models import TimeStampedModel

class Organization(TimeStampedModel):
    name = models.CharField(max_length=255)
    identifiers = models.JSONField(default=list, blank=True, help_text="""[{system, value, use, type}]""")  # [{system, value, use, type}]
    telecom = models.JSONField(default=list, blank=True, help_text="""[{system: 'phone'|'email', value}]""")      # [{system: 'phone'|'email', value}]
    address = models.JSONField(default=dict, blank=True, help_text="""{line:[...], city, state, postalCode, country}""")      # {line:[...], city, state, postalCode, country}

    def fhir_reference(self):
        return {"reference": f"Organization/{self.id}", "display": self.name}

    def __str__(self):
        return self.name