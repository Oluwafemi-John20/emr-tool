from django.urls import path
from . import views

urlpatterns = [
    path('register-organization/', views.register_organization, name='register-organization'),
]