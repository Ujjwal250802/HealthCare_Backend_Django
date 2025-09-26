from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'license_number', 'hospital_name', 'consultation_fee', 'is_active', 'created_at')
    list_filter = ('specialization', 'gender', 'is_active', 'created_at', 'years_of_experience')
    search_fields = ('first_name', 'last_name', 'email', 'license_number', 'specialization', 'hospital_name')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'gender')
        }),
        ('Professional Information', {
            'fields': ('license_number', 'specialization', 'qualification', 'years_of_experience')
        }),
        ('Hospital/Practice Information', {
            'fields': ('hospital_name', 'hospital_address', 'consultation_fee')
        }),
        ('Availability', {
            'fields': ('available_days', 'available_hours')
        }),
        ('Additional Information', {
            'fields': ('biography', 'languages_spoken', 'is_active')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )