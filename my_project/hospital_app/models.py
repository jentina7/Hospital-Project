from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


class Profile(AbstractUser):
    ROLE_CHOICES = (
        ('Администратор', 'Администратор'),
        ('Врач', 'Врач'),
        ('Пациент', 'Пациент'),
    )
    role = models.CharField(max_length=18, choices=ROLE_CHOICES)
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile_picture/", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}-{self.first_name}-{self.last_name}"


class Department(models.Model):
    department_name = models.CharField(max_length=32)
    head_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    location = models.TextField()

    def __str__(self):
        return self.department_name


class Doctor(Profile):
    SPECIALTY_CHOICES = (
        ("Стоматолог", "Стоматолог"),
        ("Педиатр", "Педиатр"),
        ("Офтальмолог", "Офтальмолог"),
        ("Невролог", "Невролог"),
        ("Хирург", "Хирург"),
        ("Гинеколог", "Гинеколог"),
        ("Кардиолог", "Кардиолог"),
        ("Терапевт", "Терапевт"),
        ("Психиатр", "Психиатр"),
        ("Онколог", "Онколог"),
        ("Косметолог", "Косметолог"),
    )
    specialty = MultiSelectField(max_length=32, choices=SPECIALTY_CHOICES, max_choices=4)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE)
    shift_start = models.DateTimeField()
    shift_end = models.DateTimeField()
    WORKING_DAYS_CHOICES = (
        ("Понедельник", "Понедельник"),
        ("Вторник", "Вторник"),
        ("Среда", "Среда"),
        ("Четверг", "Четверг"),
        ("Пятница", "Пятница"),
        ("Суббота", "Суббота"),
    )
    working_days = MultiSelectField(max_length=64, choices=WORKING_DAYS_CHOICES, max_choices=3)
    price = models.PositiveIntegerField(default=0)
    qualifications = models.TextField()
    experience_years = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.first_name}-{self.last_name} - {self.specialty}"


class PatientProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="patient_profile")
    emergency_contact = PhoneNumberField(region='KG', null=True, blank=True)
    BLOOD_CHOICES = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )
    blood_type = models.CharField(max_length=1, choices=BLOOD_CHOICES)
    allergies = models.TextField()
    medical_history = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.allergies} - {self.blood_type}"

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ("запланировано", "запланировано"),
        ("завершено", "завершено"),
        ("отменено", "отменено"),

    )
    status = models.CharField(max_length=16, choices=STATUS_CHOICES)
    notes = models.TextField()

    def __str__(self):
        return f"{self.doctor} - {self.patient} - {self.status}"


class Prescription(models.Model):
    patient = models.ManyToManyField(PatientProfile)
    doctor = models.ManyToManyField(Doctor)
    medicament = models.CharField(max_length=64)
    dosage = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor}-{self.patient}-{self.medicament}"


class MedicalRecord(models.Model):
    patient = models.ManyToManyField(PatientProfile)
    doctor = models.ManyToManyField(Doctor)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescribed_medication = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient}-{self.doctor}-{self.diagnosis}"


class Feedback(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="doctor_feedback")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True,
                                blank=True)
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.patient} - {self.doctor} - {self.rating}'

    def get_average_rating(self):
        feedback = self.feedback.all()
        if feedback.exists():
            return round(sum(feedback.rating for feedback in feedback) / feedback.count(), 1)
        return 0


class Billings(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="billings")
    total_amount = models.PositiveIntegerField(default=0)
    paid = models.BooleanField(default=False)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient} - {self.total_amount} - {self.paid}"


class Wards(models.Model):
    name = models.CharField(max_length=64)
    TYPE_WARD_CHOICES = (
        ("vip", "vip"),
        ("люкс", "люкс"),
        ("простая", "простая"),
    )
    type_ward = models.CharField(max_length=16, choices=TYPE_WARD_CHOICES, default="простая")
    capacity = models.PositiveSmallIntegerField(default=1)
    current_occupancy = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"{self.name}-{self.type_ward}-{self.capacity}"

    # def free_spaces(self):
    #     return max(0, self.capacity - self.current_occupancy)