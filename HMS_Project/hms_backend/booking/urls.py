from django.urls import path
from .views import doctor_dashboard, patient_dashboard, book_slot

urlpatterns = [
    path("doctor/dashboard/", doctor_dashboard, name="doctor_dashboard"),
    path("patient/dashboard/", patient_dashboard, name="patient_dashboard"),
    path("book/<int:slot_id>/", book_slot, name="book_slot"),
]
