from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from patients.models import Patient
from encounters.models import Encounter
from datetime import date


# Create your views here.
@login_required(login_url="/login")
def home(request):
    return render(request, 'authenticator/home.html')

def sign_up(request):
    if request.method=="POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('home'))

    else:
        form = RegisterForm()
    
    return render(request, "registration/sign_up.html", {"form": form})

@login_required
def dashboard(request):
    total_patients = Patient.objects.count()
    total_encounters = Encounter.objects.count()
    todays_encounters = Encounter.objects.filter(created_at__date=date.today()).count()
    encounters_this_month = Encounter.objects.filter(created_at__month=date.today().month).count()

    todays_patients = Patient.objects.filter(created_at__date=date.today())

    todays_encounters_list = Encounter.objects.filter(created_at__date=date.today())

    context = {
        "total_patients": total_patients,
        "total_encounters": total_encounters,
        "todays_encounters": todays_encounters,
        "encounters_this_month": encounters_this_month,
        "todays_patients": todays_patients,
        "todays_encounters_list": todays_encounters_list,
    }
    return render(request, "authenticator/home.html", context)