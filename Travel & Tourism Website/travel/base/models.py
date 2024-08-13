from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Destination(models.Model):
    id = models.IntegerField(primary_key=True)
    country = models.CharField(max_length=20)
    img1 = models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    number = models.IntegerField(default=2)

    def __str__(self):
        return f" {self.country}"

class Detailed_desc(models.Model):
    dest_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=20)
    days = models.IntegerField(default=5)
    price = models.IntegerField(default=20000)
    rating = models.IntegerField(default=5)
    dest_name = models.CharField(max_length=25)
    img1=models.ImageField(upload_to='pics')
    img2 = models.ImageField(upload_to='pics')
    desc = models.TextField()
    day1 = models.TextField()
    day2 = models.TextField()
    day3 = models.TextField()
    day4 = models.TextField()
    day5 = models.TextField()
    day6 = models.TextField()

    def __str__(self):
        return f"{self.dest_name} ({self.country})"


class Booking(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    destination = models.CharField(max_length=100)
    travel_date = models.DateField()
    number_of_people = models.IntegerField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_completed = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
   
    def __str__(self):
        return f"{self.name} - {self.destination}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Subscribers(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email