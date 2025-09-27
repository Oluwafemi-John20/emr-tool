from django.urls import path
from . import views

urlpatterns = [
    path('record-observation/patients/<int:patient_id>/encounters/<int:encounter_id>/observation/new/', views.record_observation, name='record-observation'),
]