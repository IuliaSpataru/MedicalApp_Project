from django.contrib import admin

from .models import Ward, User, Task, Patient


# Register your models here.


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'ward')
    list_filter = ('role', 'ward')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'completed', 'created_at')
    list_filter = ('completed', 'user__role', 'user__ward')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'created_at', 'updated_at')
    list_filter = ('ward',)