from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

class Doctor(models.Model):
    """
    Doctor model for storing doctor information
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    # Basic Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specialization = models.CharField(max_length=200)
    qualification = models.CharField(max_length=300)
    years_of_experience = models.PositiveIntegerField()
    
    # Hospital/Clinic Information
    hospital_name = models.CharField(max_length=300)
    hospital_address = models.TextField()
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # Availability
    available_days = models.CharField(max_length=100, help_text="e.g., Mon-Fri, Weekdays, etc.")
    available_hours = models.CharField(max_length=100, help_text="e.g., 9:00 AM - 5:00 PM")

    # Additional Information
    biography = models.TextField(blank=True)
    languages_spoken = models.CharField(max_length=200, help_text="Comma-separated languages")

    # System fields
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctors')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['specialization']),
            models.Index(fields=['license_number']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name} - {self.specialization}"

    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}".strip()