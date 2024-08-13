from django.contrib import admin
from . models import User,Add_Patient,Doctor,Appointment,ContactSubmission
# Register your models here.

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('username', 'first_name', 'last_name', 'email')

@admin.register(Add_Patient)
class AddPatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'gender', 'mobile', 'submitted_time')
    search_fields = ('name', 'mobile')
    list_filter = ('gender', 'submitted_time')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('your_name', 'phone_number', 'e_mail', 'select_date', 'gender', 'department', 'status')
    search_fields = ('your_name', 'phone_number', 'e_mail')
    list_filter = ('status', 'select_date', 'department')

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at','message')
    search_fields = ('name', 'email','message')


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'department', 'mobile', 'status')
    search_fields = ('user__first_name', 'user__last_name', 'department', 'mobile')
    list_filter = ('department', 'status')



