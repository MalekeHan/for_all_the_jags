from django.db import models

# Create your models here.

class Survey(models.Model):
    BUSY_CHOICES = [
        ('NB', 'Not busy'),
        ('MB', 'Moderately Busy'),
        ('VB', 'Very busy'),
    ]

    COMFORT_CHOICES = [
        ('VC', 'Very comfortable'),
        ('MC', 'Moderately comfortable'),
        ('NC', 'Not comfortable'),
    ]

    WIFI_CHOICES = [
        ('NW', 'No WIFI'),
        ('PW', 'WIFI, but must be paid'),
        ('FW', 'WIFI, Free'),
    ]

    NOISE_CHOICES = [
        ('QZ', 'Quiet enough for a zoom meeting'),
        ('MN', 'Moderate noise'),
        ('VN', 'Very noisy'),
    ]

    PARKING_CHOICES = [
        ('EP', 'Very easy parking'),
        ('MP', 'Moderate parking'),
        ('DP', 'Very difficult parking'),
    ]

    # Model Fields
    busy_level = models.CharField(max_length=2, choices=BUSY_CHOICES, default='NB')
    comfort_level = models.CharField(max_length=2, choices=COMFORT_CHOICES, default='VC')
    wifi_situation = models.CharField(max_length=2, choices=WIFI_CHOICES, default='NW')
    noise_level = models.CharField(max_length=2, choices=NOISE_CHOICES, default='QZ')
    parking_situation = models.CharField(max_length=2, choices=PARKING_CHOICES, default='EP')

    def __str__(self):
        return f"Survey #{self.id}"