# Generated by Django 5.0.6 on 2024-08-04 08:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_subscribers_delete_bookingformform'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Subscribers',
        ),
    ]