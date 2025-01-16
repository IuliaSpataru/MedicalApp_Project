from django.db import models
from django.db.models import *

# Create your models here.

class Ward(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class User(models.Model):
    ROLES = [
        ('CERTIFIED_NURSE', 'Certified Nurse'),
        ('LICENSED_NURSE', 'Licensed Nurse'),
        ('ATTENDING_PHYSICIAN', 'Attending Physician'),
        ('DOCTOR_ON_DUTY', 'Doctor on Duty'),
        ('HEAD_OF_DEPARTMENT', 'Head of Department'),
        ('HOSPITAL_MANAGER', 'Hospital Manager'),
    ]

    name = CharField(max_length=128)
    role = CharField(max_length=20, choices=ROLES)
    ward = ForeignKey(Ward, on_delete=DO_NOTHING, null=True, blank=True)

    def can_update_tasks(self):
        return self.role in ['LICENSED_NURSE', 'ATTENDING_PHYSICIAN', 'DOCTOR_ON_DUTY', 'HEAD_OF_DEPARTMENT', 'HOSPITAL_MANAGER']

    def can_view_reports(self):
        return self.role in ['HEAD_OF_DEPARTMENT', 'HOSPITAL_MANAGER']

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"


class Task(models.Model):
    description = TextField()
    user = ForeignKey(User, on_delete=CASCADE)
    assigned_to = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    completed = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='tasks', null=True, blank=True)
    room_number = models.CharField(max_length=10, blank=True, default='Pending')

    def save(self, *args, **kwargs):
        if not self.room_number:
            self.room_number = self.patient.room_number
        super(Task, self).save(*args, **kwargs)


    def __str__(self):
        return f"Task for patient {self.patient.name}"


class Patient(models.Model):
    name = CharField(max_length=128)
    ward = ForeignKey(Ward, on_delete=DO_NOTHING)
    created_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    room_number = IntegerField(primary_key=True, default=1)

    def __str__(self):
        return f"{self.name}"