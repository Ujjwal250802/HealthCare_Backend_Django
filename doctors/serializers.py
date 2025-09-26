from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model
    """
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number', 'gender',
            'license_number', 'specialization', 'qualification', 'years_of_experience',
            'hospital_name', 'hospital_address', 'consultation_fee', 'available_days',
            'available_hours', 'biography', 'languages_spoken', 'is_active',
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by_username', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Validate that email is unique for doctors
        """
        if self.instance:
            # If updating, exclude current instance from uniqueness check
            if Doctor.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        else:
            # If creating new doctor
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_license_number(self, value):
        """
        Validate that license number is unique
        """
        if self.instance:
            if Doctor.objects.filter(license_number=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        else:
            if Doctor.objects.filter(license_number=value).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        return value

    def validate_years_of_experience(self, value):
        """
        Validate years of experience
        """
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative.")
        if value > 60:
            raise serializers.ValidationError("Years of experience seems unrealistic.")
        return value

    def validate_consultation_fee(self, value):
        """
        Validate consultation fee
        """
        if value <= 0:
            raise serializers.ValidationError("Consultation fee must be greater than 0.")
        return value

    def create(self, validated_data):
        """
        Create doctor with the authenticated user as creator
        """
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class DoctorListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for doctor list views
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'phone_number', 'specialization', 'qualification', 
            'years_of_experience', 'hospital_name', 'consultation_fee',
            'available_days', 'is_active', 'created_at'
        ]