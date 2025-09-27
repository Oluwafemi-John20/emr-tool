from django.urls import path
from . import views

urlpatterns = [
    path('record-medications/', views.record_medications, name='record-medications'),
]