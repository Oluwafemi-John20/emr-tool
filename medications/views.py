from django.shortcuts import render, redirect
from authenticator.forms import MedicationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required
def record_medications(request):
    if request.method == 'POST':
        form = MedicationForm(request.POST)
        if form.is_valid():
            medication = form.save()
            return redirect(reverse("home"))
    else:
        form = MedicationForm()

    return render(request, "medications/record-medications.html", {"form": form})