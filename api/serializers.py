from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Doctor, Patient, PatientDoctorMapping 

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__' # Include all fields from the Doctor model


class PatientSerializer(serializers.ModelSerializer):
    # We make managed_by readonly because it should be automatically set to the logged-in user,
    # not provided by the user in the request body.
    managed_by = serializers.ReadOnlyField(source='managed_by.username')

    class Meta:
        model = Patient
        fields = '__all__'


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    # Displaying the names instead of just the IDs makes the API response more readable.
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = ('id', 'patient', 'doctor', 'patient_name', 'doctor_name', 'assigned_at')