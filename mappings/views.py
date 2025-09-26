from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer, PatientDoctorMappingListSerializer


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def mapping_list_create(request):
    """
    GET: List all patient-doctor mappings
    POST: Create a new patient-doctor mapping
    """
    if request.method == 'GET':
        mappings = PatientDoctorMapping.objects.filter(assigned_by=request.user)
        
        # Filter by status if provided
        status_filter = request.query_params.get('status')
        if status_filter:
            mappings = mappings.filter(status=status_filter.upper())
            
        serializer = PatientDoctorMappingListSerializer(mappings, many=True)
        return Response({
            'count': mappings.count(),
            'mappings': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = PatientDoctorMappingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mapping = serializer.save()
            return Response({
                'message': 'Patient-doctor mapping created successfully',
                'mapping': PatientDoctorMappingSerializer(mapping).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Mapping creation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def patient_doctors(request, patient_id):
    """
    Get all doctors assigned to a specific patient
    """
    mappings = PatientDoctorMapping.objects.filter(
        patient_id=patient_id,
        patient__created_by=request.user
    )
    
    if not mappings.exists():
        return Response({
            'message': 'No doctors found for this patient',
            'doctors': []
        }, status=status.HTTP_200_OK)
    
    serializer = PatientDoctorMappingListSerializer(mappings, many=True)
    return Response({
        'patient_id': patient_id,
        'count': mappings.count(),
        'assigned_doctors': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def mapping_detail(request, pk):
    """
    GET: Retrieve mapping details
    PUT: Update mapping
    DELETE: Remove patient-doctor mapping
    """
    mapping = get_object_or_404(PatientDoctorMapping, pk=pk, assigned_by=request.user)

    if request.method == 'GET':
        serializer = PatientDoctorMappingSerializer(mapping)
        return Response({
            'mapping': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = PatientDoctorMappingSerializer(
            mapping, 
            data=request.data, 
            context={'request': request},
            partial=True
        )
        if serializer.is_valid():
            updated_mapping = serializer.save()
            return Response({
                'message': 'Mapping updated successfully',
                'mapping': PatientDoctorMappingSerializer(updated_mapping).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Mapping update failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        mapping_info = mapping.assignment_info
        mapping.delete()
        return Response({
            'message': f'Mapping removed successfully: {mapping_info}'
        }, status=status.HTTP_204_NO_CONTENT)