from django.db import models
from django.contrib.auth import get_user_model
from patients.models import Patient
from doctors.models import Doctor

User = get_user_model()

class PatientDoctorMapping(models.Model):
    """
    Model to map patients to doctors
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_assignments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_assignments')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_made')
    
    # Assignment details
    assignment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True, help_text="Additional notes about the assignment")
    
    # Follow-up information
    next_appointment = models.DateTimeField(null=True, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('URGENT', 'Urgent'),
        ],
        default='MEDIUM'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['patient', 'doctor']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['patient']),
            models.Index(fields=['doctor']),
            models.Index(fields=['status']),
            models.Index(fields=['assignment_date']),
        ]

    def __str__(self):
        return f"{self.patient.full_name} -> {self.doctor.full_name}"

    @property
    def assignment_info(self):
        return f"Patient: {self.patient.full_name} | Doctor: {self.doctor.full_name} | Status: {self.status}"