from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserProfileSerializers(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("username", "email", "password", "first_name", "last_name",
                 "phone_number", "role")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            "user": {
                "username": instance.username,
                "email": instance.email,
            },
            'access': str(refresh.access_token),
            "refresh": str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "first_name", "last_name", "email", "role", "phone_number",
                  "profile_picture", "address", "date_of_birth"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["username", "first_name", "last_name"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["department_name", "location"]


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "department_name", "head_id", "location"]


class DoctorSerializer(serializers.ModelSerializer):
    department_name = DepartmentSerializer()
    class Meta:
        model = Doctor
        fields = ["username", "first_name", "last_name", "phone_number", "profile_picture", "specialty",
                  "department_name", "price", "experience_years",]


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = PatientProfile
        fields = ["id", "user", "emergency_contact", "blood_type", "allergies", "medical_history"]


class AppointmentSerializer(serializers.ModelSerializer):
    date_time = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Appointment
        fields = ["id", "patient", "doctor", "date_time", "status", "notes"]


class PrescriptionListSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Prescription
        fields = ["id", "patient", "doctor", "medicament", "dosage", "created_date"]


class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ["medicament", "dosage"]


class MedicalRecordSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    prescribed_medication = PrescriptionSerializer()
    class Meta:
        model = MedicalRecord
        fields = ["id", "patient", "doctor", "diagnosis", "treatment", "prescribed_medication", "created_at"]


class FeedbackSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    average_rating = serializers.SerializerMethodField()
    class Meta:
        model = Feedback
        fields = ["id", "doctor", "patient", "rating", "average_rating", "comment", "created_date"]

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class BillingsSerializer(serializers.ModelSerializer):
    issued_date = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    class Meta:
        model = Billings
        fields = ["id", "patient", "total_amount", "paid", "issued_date"]


class WardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wards
        fields = '__all__'


class DoctorDetailSerializer(serializers.ModelSerializer):
    department_name = DepartmentSerializer()
    shift_start = serializers.DateTimeField(format="%H:%M")
    shift_end = serializers.DateTimeField(format="%H:%M")
    class Meta:
        model = Doctor
        fields = ["username", "first_name", "last_name", "phone_number", "profile_picture", "specialty",
                  "department_name", "shift_start", "shift_end", "working_days", "price", "qualifications",
                  "experience_years"]
