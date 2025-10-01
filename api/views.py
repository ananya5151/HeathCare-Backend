from rest_framework import generics, status, viewsets 
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from .serializers import UserRegisterSerializer, DoctorSerializer, PatientSerializer, PatientDoctorMappingSerializer 
from .models import Doctor, Patient, PatientDoctorMapping 
from rest_framework.decorators import action

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny] # Allow any user (authenticated or not) to access this endpoint.

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DoctorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows doctors to be viewed or edited.
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can access


class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    Patients are filtered based on the logged-in user.
    """
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the patients
        for the currently authenticated user.
        """
        return Patient.objects.filter(managed_by=self.request.user)

    def perform_create(self, serializer):
        """
        Assign the current user as the one who is managing the patient.
        """
        serializer.save(managed_by=self.request.user)
        
    @action(detail=True, methods=['get'])
    def doctors(self, request, pk=None):
        """
        Returns a list of all doctors assigned to a specific patient.
        """
        try:
            patient = self.get_object()
            mappings = PatientDoctorMapping.objects.filter(patient=patient)
            doctor_ids = [mapping.doctor.id for mapping in mappings]
            doctors = Doctor.objects.filter(id__in=doctor_ids)
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({"error": "Patient not found."}, status=status.HTTP_404_NOT_FOUND)



class PatientDoctorMappingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for mapping patients to doctors.
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]