from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Doctor(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"


class Patient(models.Model):
    # Link to the user who is managing this patient record
    managed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = models.CharField(max_length=1, choices=gender_choices)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Managed by: {self.managed_by.username})"


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ensures a patient can only be assigned to a specific doctor once
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.name} assigned to Dr. {self.doctor.name}"