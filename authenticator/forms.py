from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from patients.models import Patient
from observations.models import Observation
from encounters.models import Encounter
from medications.models import Medication
from organizations.models import Organization
from conditions.models import Condition
from django.contrib.auth import get_user_model

User = get_user_model()

ROLE_CHOICES = [
    ("ADMIN", "Admin"),
    ("DOCTOR", "Doctor"),
    ("NURSE", "Nurse"),
    ("PATIENT", "Patient"),
]

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    date_of_birth = forms.DateField(required=True)
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,     # <-- valid here
        widget=forms.Select,      # optional: dropdown
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "date_of_birth", "role", "password1", "password2"]

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

class ObservationForm(forms.ModelForm):
    class Meta:
        model = Observation
        fields = '__all__'

class EcounterForm(forms.ModelForm):
    class Meta:
        model = Encounter
        fields = '__all__'

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = '__all__'

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'
    
class ConditionForm(forms.ModelForm):
    class Meta:
        model = Condition
        fields = '__all__'