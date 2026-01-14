from django.db import models

# Create your models here.

from accounts.models import DoctorProfile, PatientProfile

class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor} | {self.date} {self.start_time}-{self.end_time}"

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    slot = models.OneToOneField(AvailabilitySlot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} booked {self.slot}"

