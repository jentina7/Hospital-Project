from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import DoctorFilter
from .pagination import CustomPagination
from .permission import  CheckCRUD, CheckFeedback, CheckRole, CheckAppointments
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response


class RegisterView(generics.CreateAPIView):
    serializer_class = UserProfileSerializers

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status= status.HTTP_200_OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class DepartmentListViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentListSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter
    pagination_class = CustomPagination



class PatientProfileViewSet(viewsets.ModelViewSet):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [CheckRole]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [CheckAppointments]


class PrescriptionListViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionListSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [CheckCRUD]


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated, CheckFeedback, CheckRole]


class BillingsViewSet(viewsets.ModelViewSet):
    queryset = Billings.objects.all()
    serializer_class = BillingsSerializer


class WardsViewSet(viewsets.ModelViewSet):
    queryset = Wards.objects.all()
    serializer_class = WardsSerializer


class DoctorDetailViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorDetailSerializer

