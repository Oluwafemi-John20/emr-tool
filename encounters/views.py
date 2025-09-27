from django.shortcuts import render, redirect
from authenticator.forms import EcounterForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404
from patients.models import Patient


@login_required
def register_encounter(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        form = EcounterForm(request.POST)
        if form.is_valid():
            encounter = form.save(commit=False)
            encounter.patient = patient
            encounter.save()
            return redirect(reverse("record-observation", args=[patient_id, encounter.id]))
    else:
        form = EcounterForm(initial={"subject": patient})

    return render(request, "encounters/register_encounter.html", {"form": form, "patient":patient})
