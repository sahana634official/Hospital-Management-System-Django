from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import DoctorProfile, PatientProfile
from .email_service import send_welcome_email


# ---------------- DOCTOR SIGNUP ----------------
def doctor_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        specialization = request.POST.get("specialization")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Try another.")
            return redirect("doctor_signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        DoctorProfile.objects.create(user=user, specialization=specialization)

        # ✅ Send Welcome Email
        send_welcome_email(email, username)

        messages.success(request, "Doctor Signup Successful ✅ Please login now.")
        return redirect("doctor_login")

    return render(request, "accounts/doctor_signup.html")


# ---------------- PATIENT SIGNUP ----------------
def patient_signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        phone = request.POST.get("phone")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Try another.")
            return redirect("patient_signup")

        user = User.objects.create_user(username=username, email=email, password=password)
        PatientProfile.objects.create(user=user, phone=phone)

        # ✅ Send Welcome Email
        send_welcome_email(email, username)

        messages.success(request, "Patient Signup Successful ✅ Please login now.")
        return redirect("patient_login")

    return render(request, "accounts/patient_signup.html")


# ---------------- DOCTOR LOGIN ----------------
def doctor_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, "doctorprofile"):
            login(request, user)
            return redirect("doctor_dashboard")

        messages.error(request, "Invalid Doctor username or password!")
        return redirect("doctor_login")

    return render(request, "accounts/doctor_login.html")


# ---------------- PATIENT LOGIN ----------------
def patient_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and hasattr(user, "patientprofile"):
            login(request, user)
            return redirect("patient_dashboard")

        messages.error(request, "Invalid Patient username or password!")
        return redirect("patient_login")

    return render(request, "accounts/patient_login.html")


# ---------------- LOGOUT ----------------
def logout_page(request):
    logout(request)
    messages.success(request, "Logged out successfully ✅")
    return redirect("patient_login")