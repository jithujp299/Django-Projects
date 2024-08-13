
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required,user_passes_test
from twilio.rest import Client

from . forms import AppointmentForm, ContactForm, PatientForm, PatientUserForm,QuickPatientForm
from . models import Add_Patient, Admin, Appointment, Doctor
from . import forms,models


def Home(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'html/contactussuccess.html')
    else:
        form = ContactForm()
    return render(request, 'html/home.html', {'form': form})

def About(request):
    return render(request,"html/about.html")

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return render(request, 'html/contactussuccess.html')
    else:
        form = ContactForm()
    return render(request, 'html/contact.html', {'form': form})

def admin_signup_view(request):
    userForm = forms.AdminSigupForm(request.POST or None)
    adminForm = forms.AdminForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and userForm.is_valid() and adminForm.is_valid():
        user = userForm.save(commit=False)
        user.set_password(user.password)
        user.save()
        admin = adminForm.save(commit=False)
        admin.user = user
        admin.save()
        Group.objects.get_or_create(name='ADMIN')[0].user_set.add(user)
        return HttpResponseRedirect('adminlogin')
    return render(request, 'admin/adminsignup.html', {'userForm': userForm, 'adminForm': adminForm})

def doctor_signup_view(request):
    userForm, doctorForm = forms.DoctorUserForm(request.POST or None), forms.DoctorForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and userForm.is_valid() and doctorForm.is_valid():
        user = userForm.save()
        user.set_password(user.password)
        user.save()
        doctor = doctorForm.save(commit=False)
        doctor.user = user
        doctor.save()
        Group.objects.get_or_create(name='DOCTOR')[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request, 'doctor/doctorsignup.html', {'userForm': userForm, 'doctorForm': doctorForm})


def patient_signup_view(request):
    userForm = PatientUserForm()
    if request.method == 'POST':
        userForm = PatientUserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)
            user.save()
            Group.objects.get_or_create(name='PATIENT')[0].user_set.add(user)
            return HttpResponseRedirect('patientlogin')

    return render(request,'patient/patientsignup.html', {'userForm': userForm})

#check doctor or admin

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='ADMIN').exists()
def is_doctor(user): 
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user): 
    return user.groups.filter(name='PATIENT').exists()
  

#after login

def afterlogin_view(request):
    if is_admin(request.user):
        if models.Admin.objects.filter(user_id=request.user.id, status=True).exists() or request.user.is_superuser:
            return redirect('admin-dashboard')
        return render(request, 'admin/admin_wait_for_approval.html')
    elif is_doctor(request.user):
        if models.Doctor.objects.filter(user_id=request.user.id, status=True).exists():
            return redirect('doctor_dashboard')
        return render(request, 'doctor/doctor_wait_for_approval.html')
    elif is_patient(request.user):
        return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('home')  


#admin dashboard


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Add_Patient.objects.all().order_by('-id')

    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Add_Patient.objects.all().count()
   
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'admin/admin_dashboard.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'admin/admin_doctor.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin/admin_view_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)

    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'admin/admin_update_doctor.html',context=mydict)

#admin approve doctor


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'admin/admin_approve_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')

#admin approve admin


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_view(request):
    return render(request,'admin/admin_approve.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approval_view(request):
    pending_admins = Admin.objects.filter(status=False)
    userForm = forms.AdminSigupForm(request.POST or None)
    return render(request, 'admin/admin_approve_view.html', {'pending_admins': pending_admins,'userform':userForm})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_admin_view(request, pk):
    admin = Admin.objects.get(id=pk)
    admin.status = True
    admin.save()
    return redirect(reverse('admin-approve-admin'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_admin_view(request, pk):
    admin = Admin.objects.get(id=pk)
    user = admin.user
    user.delete()
    admin.delete()
    return redirect('admin-approve-admin')

#admin add doctor


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'admin/admin_add_doctor.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin/admin_view_doctor_specialisation.html',{'doctors':doctors})


#admin patient section

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'admin/admin_patient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    return render(request,'admin/admin_view_patient.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Patients_Record(request):
    patient = models.Add_Patient.objects.all().order_by('-id')
    return render(request, 'admin/admin_patient_records.html', {'patient':patient})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Add_Patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"succesfully added")
            return redirect('admin-add-patient')
        else:
            messages.warning(request,"something went wrong!!")
            return redirect('admin-add-patient')
    else:
        form = PatientForm()
        return render(request,'admin/admin_add_patient.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Update_Patient(request, pk):
    patient = get_object_or_404(Add_Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('admin-patient-record'))
    else:
        form = PatientForm(instance=patient)
    return render(request, 'admin/admin_add_patient.html', {'form': form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Quick_Add_Patient(request):
    if request.method == 'POST':
        form = QuickPatientForm(request.POST)
        if form.is_valid():
            messages.success(request,"succesfully added")
            form.save()
            return redirect('admin_quick_add_patient')
        else:
            messages.warning(request,"something went wrong")
            return redirect('admin_quick_add_patient')
    else:
        form = QuickPatientForm()
        return render(request,'admin/admin_quick_add_patient.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Patients_Records(request):
    patients = Add_Patient.objects.all()
    context = {'data': patients}
    return render(request, 'admin/admin_patient_records.html', context)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def Admin_Delete_patient(request,pk):
    patient=models.Add_Patient.objects.get(id=pk)
    patient.delete()
    return redirect('admin-patient-record')


#admin appoinment section


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'admin/admin_appointment.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'admin/admin_view_appointment.html',{'appointments':appointments})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'admin/admin_add_appointment.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'admin/admin_approve_appointment.html',{'appointments':appointments})


# Twilio 
TWILIO_ACCOUNT_SID = 'AC17cefbf59be7cfb0c1e64bae8582bd55'
TWILIO_AUTH_TOKEN = 'b854d1ebe430d7f3af02c7db20196198'
TWILIO_PHONE_NUMBER = '+14092160197'


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.status = True
    appointment.save()

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        phone_number_str = str(appointment.phone_number)
        message = client.messages.create(
            body="Your appointment has been approved!",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number_str
        )
        messages.success(request, 'Appointment approved and SMS sent.')
    except Exception as e:
        messages.error(request, f'Failed to send SMS: {e}')
    
    return redirect(reverse('admin-approve-appointment'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request, pk):
    appointment = get_object_or_404(Appointment, id=pk)

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        phone_number_str = str(appointment.phone_number)
        message = client.messages.create(
            body="Your appointment has been rejected.",
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number_str
        )
        messages.success(request, 'Appointment rejected and SMS sent.')
    except Exception as e:
        messages.error(request, f'Failed to send SMS: {e}')
 
    appointment.delete()
    return redirect(reverse('admin-approve-appointment'))


#doctor dashboard

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Doctor_dashboard(request):
    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    patientcount=models.Add_Patient.objects.all().count()
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(status=True, department=doctor.department).order_by('-id')
    
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'appointments':appointments,
    'doctor':doctor,
    }
    return render(request,'doctor/doctor_dashboard.html',context=mydict)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    doctor = Doctor.objects.get(user=request.user) 
    return render(request,'doctor/doctor_patient.html',{'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Doctor_Add_Patient(request):
    doctor = Doctor.objects.get(user=request.user) 
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"succesfully added")
            return redirect('add_patients')
        else:
            messages.warning(request,"something went wrong!!")
            return redirect('add_patients')
    else:
        form = PatientForm()
        return render(request,'doctor/doctor_add_patient.html',{'form':form,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Quick_Add_Patient(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    if request.method == 'POST':
        form = QuickPatientForm(request.POST)
        if form.is_valid():
            messages.success(request,"succesfully added")
            form.save()
            return redirect('quick_add_patient')
        else:
            messages.warning(request,"something went wrong")
            return redirect('quick_add_patient')
    else:
        form = QuickPatientForm()
        return render(request,'doctor/quick_add_patient.html',{'form':form,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Delete_patient(request,pk):
    patient=models.Add_Patient.objects.get(id=pk)
    patient.delete()
    return redirect('patients_records')


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Patients_Record(request):
    patient = models.Add_Patient.objects.all().order_by('-id')
    doctor=models.Doctor.objects.get(user=request.user)
    context = {
        'patient': patient,
        'doctor': doctor
    }
    return render(request, 'doctor/patients_records.html', context)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def Update_Patient(request, pk):
    patient = get_object_or_404(Add_Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('patients_records'))
    else:
        form = PatientForm(instance=patient)
    return render(request, 'doctor/doctor_add_patient.html', {'form': form})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    return render(request,'doctor/doctor_appointment.html',{'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor = Doctor.objects.get(user=request.user)
    appointments = Appointment.objects.filter(status=True, department=doctor.department)
    return render(request, 'doctor/doctor_view_appointment.html', {'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'doctor/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.delete()
    messages.success(request, 'Appointment deleted successfully.')
    return redirect(reverse('doctor-delete-appointment'))

#patient appointment

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Appointment created successfully, for further information we will contact you soon !')
            return render(request, 'html/appointment_sucess.html')
        else:
            messages.error(request, 'Error creating appointment. Please correct the errors below.')
    else:
        form = AppointmentForm()
    return render(request, 'html/appointment.html', {'form': form})





