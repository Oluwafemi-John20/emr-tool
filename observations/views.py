from django.shortcuts import render, redirect, get_object_or_404
from authenticator.forms import ObservationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from patients.models import Patient
from encounters.models import Encounter
from authenticator.models import User

@login_required
def record_observation(request, patient_id, encounter_id):
    user = request.user
    patient = get_object_or_404(Patient, id=patient_id)
    encounter = get_object_or_404(Encounter, id=encounter_id)

    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            observation = form.save(commit=False)
            observation.performer = user
            observation.patient = patient
            observation.encounter = encounter
            observation.save()
            return redirect(reverse("record-conditions", args=[patient_id, encounter_id]))
    else:
        form = ObservationForm(initial={"performer": user, "patient": patient, "encounter": encounter})

    return render(request, "observations/record-observations.html", {"form": form,"performer": user, "patient": patient, "encounter": encounter})