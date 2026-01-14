from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ Home page → Auto redirect to Patient Login
    path("", RedirectView.as_view(url="/login/patient/", permanent=False), name="home"),

    path("", include("accounts.urls")),
    path("", include("booking.urls")),
]
print("\n✅ HMS Links:")
print("👉 Patient Signup : http://127.0.0.1:8000/signup/patient/")
print("👉 Doctor Signup  : http://127.0.0.1:8000/signup/doctor/")
print("👉 Patient Login  : http://127.0.0.1:8000/login/patient/")
print("👉 Doctor Login   : http://127.0.0.1:8000/login/doctor/\n")
