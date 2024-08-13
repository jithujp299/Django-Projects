
from django.urls import path

from . views import CustomLoginView,RegisterPage
from .import views


urlpatterns = [
    path('',views.Home,name='home'),
    path('accounts/login/',views.CustomLoginView, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('register/',views.RegisterPage, name='register'),
    
    path('about/', views.About, name='about'),
    path('packages/',views.Packages,name='packages'),
    path('packages/destination_list/<str:country>/', views.destination_list, name='destination_list'),
    
    path('booking_form/<int:dest_id>/', views.booking_form, name='booking_form'),
    path('book/', views.book_trip, name='book_trip'),
    path('payment/', views.payment_view, name='payment'),
    path('fake-payment/', views.fake_payment, name='fake_payment'),
    path('payment-successful/<int:booking_id>/', views.payment_successful, name='payment_successful'),

    path('search', views.search, name='search'),
    path('upcoming_trips/', views.upcoming_trips, name='upcoming_trips'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),

    path('add-review/', views.add_review, name='add_review'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    
]