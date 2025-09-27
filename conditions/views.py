from django.shortcuts import render, redirect, get_object_or_404
from authenticator.forms import ConditionForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from patients.models import Patient
from encounters.models import Encounter
from conditions.models import Condition
from medications.models import MedicationRequest
from observations.models import Observation


@login_required
def record_conditions(request, patient_id, encounter_id):
    user = request.user
    patient = get_object_or_404(Patient, id=patient_id)
    encounter = get_object_or_404(Encounter, id=encounter_id)

    if request.method == 'POST':
        form = ConditionForm(request.POST)
        if form.is_valid():
            condition = form.save(commit=False)
            condition.subject = patient
            condition.encounter = encounter
            condition.recorder = user
            
            return redirect(reverse("record-medications"))
    else:
        form = ConditionForm(initial={"recorder": user,
                                      "subject": patient,
                                      "encounter": encounter})

    return render(request, "conditions/record-conditions.html", {"form": form,
                                                                 "recorder": user,
                                                                 "subject": patient,
                                                                 "encounter": encounter})

@login_required
def condition_history(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    encounters = Encounter.objects.filter(subject=patient)
    medications = MedicationRequest.objects.filter(subject=patient)
    conditions = Condition.objects.filter(subject=patient)
    observations = Observation.objects.filter(patient=patient)


    context = {
        "patient": patient,
        "encounters": encounters,
        "medications": medications,
        "condition": conditions,
        "observation": observations,
    }
    return render(request, "conditions/condition-history.html", context)