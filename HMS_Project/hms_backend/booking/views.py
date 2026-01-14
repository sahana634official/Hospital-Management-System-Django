from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from datetime import date

from .models import AvailabilitySlot, Appointment
from accounts.email_service import send_booking_email_patient, send_booking_email_doctor


# ---------------- DOCTOR DASHBOARD ----------------
@login_required
def doctor_dashboard(request):
    if not hasattr(request.user, "doctorprofile"):
        messages.error(request, "Access denied! Doctor only.")
        return redirect("patient_dashboard")

    doctor = request.user.doctorprofile

    if request.method == "POST":
        slot_date = request.POST.get("date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        AvailabilitySlot.objects.create(
            doctor=doctor,
            date=slot_date,
            start_time=start_time,
            end_time=end_time,
        )
        messages.success(request, "Slot added successfully ✅")
        return redirect("doctor_dashboard")

    slots = AvailabilitySlot.objects.filter(doctor=doctor).order_by("date", "start_time")
    bookings = Appointment.objects.filter(slot__doctor=doctor).select_related("patient", "slot").order_by("-id")

    return render(request, "booking/doctor_dashboard.html", {"slots": slots, "bookings": bookings})


# ---------------- PATIENT DASHBOARD ----------------
@login_required
def patient_dashboard(request):
    if not hasattr(request.user, "patientprofile"):
        messages.error(request, "Access denied! Patient only.")
        return redirect("doctor_dashboard")

    today = date.today()
    slots = AvailabilitySlot.objects.filter(date__gte=today, is_booked=False).order_by("date", "start_time")

    return render(request, "booking/patient_dashboard.html", {"slots": slots})


# ---------------- BOOK SLOT ----------------
@login_required
def book_slot(request, slot_id):
    if not hasattr(request.user, "patientprofile"):
        messages.error(request, "Only patients can book.")
        return redirect("doctor_dashboard")

    patient = request.user.patientprofile

    with transaction.atomic():
        slot = AvailabilitySlot.objects.select_for_update().get(id=slot_id)

        if slot.is_booked:
            messages.error(request, "Slot already booked ❌")
            return redirect("patient_dashboard")

        slot.is_booked = True
        slot.save()

        Appointment.objects.create(patient=patient, slot=slot)

        # ✅ Send Emails to BOTH patient and doctor (with calendar invite .ics)
        send_booking_email_patient(request.user, slot.doctor.user, slot)
        send_booking_email_doctor(request.user, slot.doctor.user, slot)

    messages.success(request, "Booking confirmed ✅")
    return redirect("patient_dashboard")
