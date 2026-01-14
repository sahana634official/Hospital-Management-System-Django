from django.urls import path
from .views import doctor_signup, patient_signup, doctor_login, patient_login, logout_page

urlpatterns = [
    path("", patient_login, name="home"),  # homepage opens patient login

    path("signup/doctor/", doctor_signup, name="doctor_signup"),
    path("signup/patient/", patient_signup, name="patient_signup"),

    path("login/doctor/", doctor_login, name="doctor_login"),
    path("login/patient/", patient_login, name="patient_login"),

    path("logout/", logout_page, name="logout_page"),
]
