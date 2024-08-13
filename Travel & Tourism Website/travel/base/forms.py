from django import forms
from .models import Booking, Detailed_desc, Review, Subscribers

class DateField(forms.DateField):
    input_type='date'


class BookingForms(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'travel_date', 'number_of_people']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title', 'content', 'rating']



class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscribers
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email',
                'class': 'email',
                'autocapitalize': 'none',
                'autocomplete': 'off'
            }),
        }