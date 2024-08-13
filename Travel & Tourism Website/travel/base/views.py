
import random
from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView,FormView

from .forms import BookingForms, ReviewForm, SubscriberForm
from .models import Booking, Destination, Detailed_desc, Review
from django.views.generic import TemplateView

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm

from . import models
from datetime import date
from django.contrib import messages
# Create your views here.



def CustomLoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'html/login.html', {'form': form})


def RegisterPage(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect(reverse_lazy('home'))
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    if request.user.is_authenticated:
        return redirect('home')
    
    return render(request, 'html/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')



def Home(request):
    dests = Destination.objects.all()
    dest1 = Detailed_desc.objects.all()
    return render(request, 'html/home.html', {'dests': dests, 'dest1': dest1})

def Packages(request):
    dests = Destination.objects.all()
    return render(request, 'html/package.html', {'dests': dests})


def About(request):
    reviews = Review.objects.all()
    return render(request, 'html/about.html', {'reviews': reviews})


def destination_list(request, city_name):
    dests = Detailed_desc.objects.filter(country=city_name)
    return render(request, 'html/travel_destination.html', {'dests': dests})

def destination_details(request,city_name):
    dest = Detailed_desc.objects.get(dest_name=city_name)
    price = dest.price
    request.session['price'] = price
    request.session['city'] = city_name
    return render(request,'html/destination_details.html',{'dest':dest})

def search(request):
    query = request.GET.get('q')
    if query:
        try:
            dest = Detailed_desc.objects.get(dest_name=query)
            return render(request, 'html/destination_details.html', {'dest': dest})
        except Detailed_desc.DoesNotExist:
            messages.info(request, 'Place not found')
    else:
        messages.info(request, 'Please enter a search query')
    return redirect('home')



@login_required
def upcoming_trips(request):
    today = date.today()
    bookings = Booking.objects.filter(user=request.user, travel_date__gte=today).order_by('travel_date')
    return render(request, 'html/upcoming_trips.html', {'bookings': bookings})



@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.user != request.user:
        return redirect('home')  
    
    return render(request, 'html/booking_detail.html', {'booking': booking})

@login_required
def booking_form(request, dest_id):
    try:
        destination = Detailed_desc.objects.get(dest_id=dest_id)
    except Detailed_desc.DoesNotExist:
        return redirect('home')

    form = BookingForms()
    return render(request, 'html/booking_form.html', {'form': form, 'destination': destination})


@login_required
def book_trip(request):
    if request.method == 'POST':
        destination_id = request.POST.get('destination')
        destination = get_object_or_404(Detailed_desc, dest_id=destination_id)
        
        form = BookingForms(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.destination = destination  
            booking.user = request.user  
            
            # Calculate payment amount
            price_per_person = destination.price
            total_price = booking.number_of_people * price_per_person
            gst = total_price * 0.18
            final_total = total_price + gst
            booking.payment_amount = final_total
            booking.save()
            
            # Pass payment details to the template
            context = {
                'name': booking.name,
                'destination': destination.dest_name,
                'travel_date': booking.travel_date,
                'number_of_people': booking.number_of_people,
                'total_price': total_price,
                'gst': gst,
                'final_total': final_total
            }
           
            return render(request, 'html/payment.html', context)
        else:
            return render(request, 'html/booking_form.html', {'form': form, 'destination': destination})
    else:
        return redirect('home') 


@login_required
def fake_payment(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        booking = Booking.objects.filter(user=request.user).last()  
        
        payment_successful = True
        
        if payment_successful:
            return render(request, 'html/payment_success.html', {'amount': amount, 'booking': booking})
        else:
            return render(request, 'html/payment_failed.html', {'amount': amount})
    else:
        return redirect('home')

@login_required
def payment_successful(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    context = {
        'booking': booking,
        'user': request.user,
    }
    return render(request, 'html/payment_successful.html', context)    


@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'html/payment.html', {'booking': booking})

def review_list(request):
    reviews = models.Review.objects.all()
    return render(request, 'html/about.html', {'reviews': reviews})

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('about')
        else:
            messages.error(request, 'Failed to submit review. Please check the form for errors.')
    else:
        form = ReviewForm()
    
    return render(request, 'html/home.html', {'form': form})


def subscribe(request):
    if request.method == 'POST':
        forms = SubscriberForm(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, 'Subscribed successfully!')
            return redirect('home')  
        else:
            messages.error(request, 'Subscription failed. Please enter a valid email.')
    else:
        forms = SubscriberForm()
    
    return render(request, 'html/home.html', {'forms': forms})