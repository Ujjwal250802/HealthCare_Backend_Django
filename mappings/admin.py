from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'status', 'priority', 'assignment_date', 'next_appointment', 'assigned_by')
    list_filter = ('status', 'priority', 'assignment_date', 'doctor__specialization')
    search_fields = ('patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name')
    readonly_fields = ('assignment_date', 'created_at', 'updated_at')
    list_editable = ('status', 'priority')
    
    fieldsets = (
        ('Assignment Details', {
            'fields': ('patient', 'doctor', 'assigned_by', 'assignment_date')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'notes')
        }),
        ('Follow-up Information', {
            'fields': ('next_appointment',)
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('patient', 'doctor', 'assigned_by')