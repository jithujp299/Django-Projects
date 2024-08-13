
from django import forms
from . models import  Admin, ContactSubmission, User,Add_Patient, Appointment
from django.forms import ModelForm
from phonenumber_field.formfields import PhoneNumberField
from . import models


class QuickPatientForm(ModelForm):
    class Meta:
        model = Add_Patient
        fields = ["name","gender","mobile","medcine_detail","amount"]

    def __init__(self,*args, **kwargs):
        super(QuickPatientForm,self).__init__(*args, **kwargs)
        self.fields['medcine_detail'].widget.attrs['rows']='5'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class PatientForm(ModelForm):
    class Meta:
        model = Add_Patient
        fields = ["name","age","gender","mobile","address","medcine_detail","amount","note"]
    def __init__(self,*args, **kwargs):
        super(PatientForm,self).__init__(*args, **kwargs)
        self.fields['medcine_detail'].widget.attrs['rows']='3'
        self.fields['address'].widget.attrs['rows']='3'
        self.fields['note'].widget.attrs['rows']='3'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'


class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']


class AdminForm(forms.ModelForm):
    class Meta:
       model = Admin
       fields = ['address','mobile']

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


class AppointmentForm(forms.ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Phone',
        'required': 'required'
    }))
    
    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].initial = '+91   '
        

    class Meta:
        model = Appointment
        fields = ['your_name', 'phone_number', 'e_mail', 'select_date', 'gender', 'department', 'description']

        widgets = {
            'your_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': 'required'
            }),
            'e_mail': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email',
                'required': 'required'
            }),
            'select_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'placeholder': 'Select Date'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select a department'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Message',
                'style': 'height: 10rem;'
            }),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
