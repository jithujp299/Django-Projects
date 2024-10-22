# Generated by Django 5.0.6 on 2024-08-04 06:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=20)),
                ('img1', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(upload_to='pics')),
                ('number', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Detailed_desc',
            fields=[
                ('dest_id', models.AutoField(primary_key=True, serialize=False)),
                ('country', models.CharField(max_length=20)),
                ('days', models.IntegerField(default=5)),
                ('price', models.IntegerField(default=20000)),
                ('rating', models.IntegerField(default=5)),
                ('dest_name', models.CharField(max_length=25)),
                ('img1', models.ImageField(upload_to='pics')),
                ('img2', models.ImageField(upload_to='pics')),
                ('desc', models.TextField()),
                ('day1', models.CharField(max_length=200)),
                ('day2', models.CharField(max_length=200)),
                ('day3', models.CharField(max_length=200)),
                ('day4', models.CharField(max_length=200)),
                ('day5', models.CharField(max_length=200)),
                ('day6', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('destination', models.CharField(max_length=100)),
                ('travel_date', models.DateField()),
                ('number_of_people', models.IntegerField()),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookingForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=200)),
                ('Email', models.EmailField(max_length=254)),
                ('Phone', models.FloatField()),
                ('Address', models.CharField(max_length=500)),
                ('Where_To', models.CharField(max_length=160)),
                ('How_Many', models.FloatField()),
                ('Arrival', models.DateField()),
                ('Leaving', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
