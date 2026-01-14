from django import forms
from django.contrib.auth.models import User

class DoctorSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    specialization = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

class PatientSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]
