from django import forms

class PatientSearchForm(forms.Form):
    identifier = forms.CharField(label="Patient ID or Name", max_length=100)
