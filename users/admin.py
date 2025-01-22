from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.html import format_html
from django import forms
from .models import Ward, User, Task, Patient


# Register your models here.

class WardAdminForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ['name', 'head_of_department', 'team_members']

    def __init__(self, *args, **kwargs):
        super(WardAdminForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            ward = kwargs['instance']
            self.fields['team_members'].queryset = User.objects.filter(ward=ward)




@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    form = WardAdminForm

    list_display = ('name', 'head_of_department', )
    search_fields = ('name',)
    list_filter = ('name', 'head_of_department', 'team_members')

    fieldsets = (
        (None, {
            'fields': ('name', 'head_of_department', 'team_members')
        }),
    )

    def get_team_members(self, obj):
        team_members = obj.team_members.all()
        return ", ".join([user.name for user in team_members])

    get_team_members.short_description = 'Team Members'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'ward', 'head_of_department')
    list_filter = ('role', 'ward')
    list_per_page = 15

    def head_of_department(self, obj):
        if obj.ward and obj.ward.head_of_department:
            return obj.ward.head_of_department.name
        return None

    head_of_department.short_description = 'Head of Department'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'user', 'completed', 'created_at')
    list_filter = ('completed', 'user__role', 'user__ward')
    list_per_page = 5


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward', 'admitted_at', 'updated_at')
    list_filter = ('ward',)
    list_per_page = 10

