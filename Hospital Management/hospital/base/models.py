from django.db import models
from django.contrib.auth.models import AbstractUser,User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class User(AbstractUser):
    pass

GENDER_CHOICES = (
    ('male','Male'),
    ('female','Female'),
    ('other','Other'),
)

departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]


class Add_Patient(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default='male')
    mobile = models.IntegerField(null=True)
    address = models.TextField(null=True)
    medcine_detail = models.TextField(null=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    note = models.TextField(null=True)
    submitted_time = models.DateTimeField(auto_now_add=True,null=True)
  
    def __str__(self):
        return f"{self.name}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20, null=True)
    status = models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def get_id(self):
        return self.user.id

    def __str__(self):
        return "{} (Admin)".format(self.user.first_name)

class Doctor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department = models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status = models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)


class Appointment(models.Model):
    your_name = models.CharField(max_length=40,null=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    subitted_date = models.DateTimeField(auto_now=True)
    e_mail = models.CharField(max_length=50,null=True)
    select_date = models.DateField()
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,default='male')
    department = models.CharField(max_length=50,choices=departments,default='Cardiologist')
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Appointment for {self.your_name} on {self.select_date}"


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"