from django.shortcuts import render, redirect, get_object_or_404
from authenticator.forms import PatientForm
from authenticator.models import User
from django.contrib.auth.decorators import login_required
from .models import Patient
from encounters.models import Encounter
from medications.models import Medication, MedicationRequest
from observations.models import Observation
from django.urls import reverse
from .forms import PatientSearchForm
from django.db.models import Q

@login_required
def create_patient(request):

    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=True)
            return redirect(reverse("register-encounter", kwargs={"patient_id": patient.id}))
    else:
        form = PatientForm()

    return render(request, 'patients/create_patient.html', {'form': form})

@login_required
def patient_history(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    encounters = Encounter.objects.filter(subject=patient)
    medications = MedicationRequest.objects.filter(subject=patient)
    observations = Observation.objects.filter(patient=patient)

    context = {
        "patient": patient,
        "encounters": encounters,
        "medications": medications,
        "observations": observations,
    }
    return render(request, "patients/patient-history.html", context)

@login_required
def patient_search(request):
    form = PatientSearchForm(request.GET or None)
    patient = None

    if form.is_valid():
        identifier = form.cleaned_data["identifier"].strip()

        # build query: search name (case-insensitive) and id (if numeric)
        query = Q(name__icontains=identifier)
        if identifier.isdigit():
            query |= Q(id=int(identifier))

        patient = Patient.objects.filter(query).first()

        if patient:
            return redirect("patient_history", patient_id=patient.id)

    return render(request, "patients/patient_search.html", {"form": form, "patient": patient})





