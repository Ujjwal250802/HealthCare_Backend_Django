from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Patient
from .serializers import PatientSerializer, PatientListSerializer


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def patient_list_create(request):
    """
    GET: List all patients created by authenticated user
    POST: Create a new patient
    """
    if request.method == 'GET':
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientListSerializer(patients, many=True)
        return Response({
            'count': patients.count(),
            'patients': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            patient = serializer.save()
            return Response({
                'message': 'Patient created successfully',
                'patient': PatientSerializer(patient).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Patient creation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def patient_detail(request, pk):
    """
    GET: Retrieve patient details
    PUT: Update patient information
    DELETE: Delete patient
    """
    patient = get_object_or_404(Patient, pk=pk, created_by=request.user)

    if request.method == 'GET':
        serializer = PatientSerializer(patient)
        return Response({
            'patient': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PatientSerializer(patient, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_patient = serializer.save()
            return Response({
                'message': 'Patient updated successfully',
                'patient': PatientSerializer(updated_patient).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Patient update failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        patient_name = patient.full_name
        patient.delete()
        return Response({
            'message': f'Patient {patient_name} deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)