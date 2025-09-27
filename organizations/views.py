from django.shortcuts import render
from django.shortcuts import render, redirect
from authenticator.forms import OrganizationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def register_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            organization = form.save()
            return redirect(reverse("home"))
    else:
        form = OrganizationForm()

    return render(request, "organizations/register-organization.html", {"form": form})
