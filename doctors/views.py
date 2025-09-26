from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Doctor
from .serializers import DoctorSerializer, DoctorListSerializer


@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def doctor_list_create(request):
    """
    GET: List all doctors (public access for all authenticated users)
    POST: Create a new doctor
    """
    if request.method == 'GET':
        doctors = Doctor.objects.filter(is_active=True)
        
        # Filter by specialization if provided
        specialization = request.query_params.get('specialization')
        if specialization:
            doctors = doctors.filter(specialization__icontains=specialization)
            
        serializer = DoctorListSerializer(doctors, many=True)
        return Response({
            'count': doctors.count(),
            'doctors': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = DoctorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor created successfully',
                'doctor': DoctorSerializer(doctor).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'error': 'Doctor creation failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def doctor_detail(request, pk):
    """
    GET: Retrieve doctor details (public access for all authenticated users)
    PUT: Update doctor information (only creator can update)
    DELETE: Delete doctor (only creator can delete)
    """
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'GET':
        serializer = DoctorSerializer(doctor)
        return Response({
            'doctor': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # Only creator can update
        if doctor.created_by != request.user:
            return Response({
                'error': 'You do not have permission to update this doctor'
            }, status=status.HTTP_403_FORBIDDEN)
            
        serializer = DoctorSerializer(doctor, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_doctor = serializer.save()
            return Response({
                'message': 'Doctor updated successfully',
                'doctor': DoctorSerializer(updated_doctor).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Doctor update failed',
            'details': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Only creator can delete
        if doctor.created_by != request.user:
            return Response({
                'error': 'You do not have permission to delete this doctor'
            }, status=status.HTTP_403_FORBIDDEN)
            
        doctor_name = doctor.full_name
        doctor.delete()
        return Response({
            'message': f'Doctor {doctor_name} deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)