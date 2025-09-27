from django.urls import path
from . import views
# register-encounter/
urlpatterns = [
    path('patients/<int:patient_id>/encounters/new/', views.register_encounter, name='register-encounter'),
]