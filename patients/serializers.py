from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    full_name = serializers.ReadOnlyField()
    full_address = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'blood_group', 'address_line_1', 'address_line_2',
            'city', 'state', 'postal_code', 'country', 'full_address', 'medical_history',
            'allergies', 'emergency_contact_name', 'emergency_contact_phone',
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by_username', 'created_at', 'updated_at']

    def validate_email(self, value):
        """
        Validate that email is unique for patients
        """
        if self.instance:
            # If updating, exclude current instance from uniqueness check
            if Patient.objects.filter(email=value).exclude(id=self.instance.id).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        else:
            # If creating new patient
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        return value

    def create(self, validated_data):
        """
        Create patient with the authenticated user as creator
        """
        request = self.context.get('request')
        validated_data['created_by'] = request.user
        return super().create(validated_data)


class PatientListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for patient list views
    """
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 
            'phone_number', 'date_of_birth', 'gender', 'blood_group',
            'city', 'created_by_username', 'created_at'
        ]