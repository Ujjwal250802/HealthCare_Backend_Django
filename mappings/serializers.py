from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.serializers import PatientListSerializer
from doctors.serializers import DoctorListSerializer


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model
    """
    patient_details = PatientListSerializer(source='patient', read_only=True)
    doctor_details = DoctorListSerializer(source='doctor', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    assignment_info = serializers.ReadOnlyField()

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_details', 'doctor_details',
            'assigned_by_username', 'assignment_date', 'status', 'notes',
            'next_appointment', 'priority', 'assignment_info',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'assigned_by_username', 'assignment_date', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Validate the patient-doctor mapping
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if patient belongs to the current user
        request = self.context.get('request')
        if patient and patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign your own patients to doctors.")
            
        # Check if mapping already exists (for create only)
        if not self.instance and PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
            
        return attrs

    def create(self, validated_data):
        """
        Create mapping with the authenticated user as assigner
        """
        request = self.context.get('request')
        validated_data['assigned_by'] = request.user
        return super().create(validated_data)


class PatientDoctorMappingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for mapping list views
    """
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient_name', 'doctor_name', 'doctor_specialization',
            'assigned_by_username', 'status', 'priority', 'assignment_date',
            'next_appointment', 'created_at'
        ]