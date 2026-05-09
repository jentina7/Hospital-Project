from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"profile", ProfileViewSet, basename="profile-list"),
router.register(r"department", DepartmentListViewSet, basename="department-list"),
router.register(r"doctor", DoctorViewSet, basename="doctor-list"),
router.register(r"doctor-detail", DoctorDetailViewSet, basename="doctor-detail"),
router.register(r"patient", PatientProfileViewSet, basename="patient-list"),
router.register(r"appointment", AppointmentViewSet, basename="appointment-list"),
router.register(r"prescription", PrescriptionListViewSet, basename="prescription-list"),
router.register(r"medical_record", MedicalRecordViewSet, basename="medical_record-list"),
router.register(r"feedback", FeedbackViewSet, basename="feedback-list"),
router.register(r"billings", BillingsViewSet, basename="billings-list"),
router.register(r"wards", WardsViewSet, basename="wards-list")


urlpatterns = [
    path("", include(router.urls)),

    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]