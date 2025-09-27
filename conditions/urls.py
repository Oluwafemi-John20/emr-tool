from django.urls import path
from . import views

urlpatterns = [
    path('patient/<int:patient_id>/encounter/<int:encounter_id>/record-conditions/', views.record_conditions, name='record-conditions'),
    path("condition/<int:patient_id>/", views.condition_history, name="condition_history")
]