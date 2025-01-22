from django.db import models
from django.db.models import *

# Create your models here.

class Ward(models.Model):
    name = models.CharField(max_length=128)
    head_of_department = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='head_of_department_of_ward'
    )
    team_members = models.ManyToManyField(
        'User',
        related_name='team_members_of_ward',
        blank=True
    )

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


class Patient(models.Model):
    name = CharField(max_length=128)
    ward = ForeignKey(Ward, on_delete=DO_NOTHING)
    admitted_at = DateField(auto_now_add=True)
    updated_at = DateField(auto_now=True)
    room_number = IntegerField(primary_key=True, default=1)

    def __str__(self):
        return f"{self.name}"


class Task(models.Model):
    description = models.TextField()
    user = models.ForeignKey(
        'User',
        on_delete=CASCADE,
        related_name='tasks_created'
    )
    assigned_to = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    related_name='tasks_assigned'
    )
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    patient = models.ForeignKey(
        'Patient',
        on_delete=models.CASCADE,
        related_name='tasks',
        null=True,
        blank=True,
    )
    room_number = models.CharField(max_length=10, blank=True, default='Pending')

    def save(self, *args, **kwargs):
        if not self.room_number:
            self.room_number = self.patient.room_number
        super(Task, self).save(*args, **kwargs)


    def __str__(self):
        return f"Task for patient {self.patient.name}"



