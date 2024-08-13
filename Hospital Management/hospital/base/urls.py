from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('logout/', views.user_logout, name='logout'),
    
    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),

    path('adminlogin', LoginView.as_view(template_name='admin/adminlogin.html'),name='adminlogin'),
    path('doctorlogin', LoginView.as_view(template_name='doctor/doctorlogin.html'),name="doctorlogin"),
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html'),name='patientlogin'),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    
    path('',views.Home,name='home' ),
    path('about/',views.About,name='about' ),
    path('contactus/',views.contact_us, name='contactus'),
    
    path('delete-appointment/<int:pk>/', views.delete_appointment_view, name='delete_appointment'),

    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),
    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),
    path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),

    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve/<int:appointment_id>/',views.approve_appointment, name='approve_appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),

    path('admin-approve', views.admin_approve_view,name='admin-approve'),
    path('admin-approve-admin/', views.admin_approval_view, name='admin-approve-admin'),
    path('approve-admin/<int:pk>/', views.approve_admin_view, name='approve-admin'),
    path('reject-admin/<int:pk>/', views.reject_admin_view, name='reject-admin'),

    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('admin-add-patient', views.Admin_Add_Patient,name='admin-add-patient'),
    path('admin-patient-record',views.Admin_Patients_Record,name='admin-patient-record'),
    path('admin-update-patient/<int:pk>/',views.Admin_Update_Patient,name='admin-update-patient'),
    path('admin-patient-delete/<int:pk>/', views.Admin_Delete_patient,name='admin_delete_patient'),
    path('admin-quick-add-patient', views.Admin_Quick_Add_Patient, name='admin_quick_add_patient'),

    
    path('doctor/doctor_dashboard', views.Doctor_dashboard, name='doctor_dashboard'),
    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor/quick_add_patient', views.Quick_Add_Patient, name='quick_add_patient'),
    path('patients_records',views.Patients_Record, name='patients_records'),
    path('doctor_add_patient',views.Doctor_Add_Patient, name='add_patients'),
    path('doctor/patient-delete/<int:pk>/', views.Delete_patient,name='delete_patient'),
    path('update_patient/<int:pk>/', views.Update_Patient, name='update_patient'),
    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),

    path('create_appoinment/',views.create_appointment, name='create_appointment'),
    
   
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


