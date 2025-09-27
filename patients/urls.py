from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.patient_search, name="patient_search"),
    path('create-patients/', views.create_patient, name='create-patients'),
    path("<int:patient_id>/history/", views.patient_history, name="patient_history"),
]