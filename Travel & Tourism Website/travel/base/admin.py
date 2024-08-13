from django.contrib import admin
from . models import Booking, Destination, Detailed_desc,Review, Subscribers
# Register your models here.

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'number', 'img1', 'img2')
    list_editable = ('country', 'number', 'img1', 'img2')
    search_fields = ('country',)
    list_filter = ('country',)
    ordering = ('country',)

@admin.register(Detailed_desc)
class DetailedDescAdmin(admin.ModelAdmin):
    list_display = ('dest_id', 'dest_name', 'country', 'days', 'price', 'rating', 'img1', 'img2')
    list_editable = ('dest_name', 'country', 'days', 'price', 'rating', 'img1', 'img2')
    search_fields = ('dest_name', 'country')
    list_filter = ('country', 'days', 'price', 'rating')
    ordering = ('country',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'rating', 'created_at')
    list_editable = ('title', 'rating')
    search_fields = ('title', 'user__username')
    list_filter = ('rating', 'created_at')
    ordering = ('-created_at',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user','name', 'destination', 'travel_date','created_at', 'number_of_people', 'payment_amount')
    list_editable = ('travel_date', 'number_of_people')
    search_fields = ('user__username', 'destination__dest_name','created_at')
    list_filter = ('travel_date', 'destination')
   
@admin.register(Subscribers)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)