from datetime import datetime
from django.db import models
from django.db.models.aggregates import Avg
from django.utils import timezone
from django.db.models import F, FloatField, ExpressionWrapper
from django.db.models.functions import Now, Extract
from django.utils.timezone import make_aware

# Create your models here.

## Location of the Spot
class Location(models.Model):
    name = models.CharField(max_length=255)
    lat = models.FloatField(default=0.0)
    lon = models.FloatField(default=0.0)
    yelp_id = models.CharField(max_length=255)

class Survey(models.Model):
    BUSY_CHOICES = [
        (0, 'Very busy'),
        (1, 'Moderately Busy'),
        (2, 'Not busy'),
    ]

    COMFORT_CHOICES = [
        (0, 'Not comfortable'),
        (1, 'Moderately comfortable'),
        (2, 'Very comfortable'),
    ]

    WIFI_CHOICES = [
        (0, 'No WIFI'),
        (1, 'WIFI, but must be paid'),
        (2, 'WIFI, Free'),
    ]

    NOISE_CHOICES = [
        (0, 'Very noisy'),
        (1, 'Moderate noise'),
        (2, 'Quiet enough for a zoom meeting'),
    ]

    PARKING_CHOICES = [
        (0, 'Very difficult parking'),
        (1, 'Moderate parking'),
        (2, 'Very easy parking'),
    ]

    
    # Defualt values are None becuase some survey responses may not have all the fields
    # Model Fields
    # busy_level = models.IntegerField(choices=BUSY_CHOICES, default=None)
    # busy_str = models.CharField(choices=BUSY_CHOICES, default=None)

    # comfort_level = models.IntegerField(choices=COMFORT_CHOICES, default=None)
    # comfort_str = models.CharField(choices=COMFORT_CHOICES, default=None)

    # wifi_situation = models.IntegerField(choices=WIFI_CHOICES, default=None)
    # wifi_str = models.CharField(choices=WIFI_CHOICES, default=None)
    
    # noise_level = models.IntegerField(choices=NOISE_CHOICES, default=None)
    # noise_str = models.CharField(choices=NOISE_CHOICES, default=None)

    # parking_situation = models.IntegerField(choices=PARKING_CHOICES, default=None)
    # parking_str = models.CharField(choices=PARKING_CHOICES, default=None)

    busy_level = models.IntegerField(choices=BUSY_CHOICES, default=None, null=True, blank=True)
    comfort_level = models.IntegerField(choices=COMFORT_CHOICES, default=None, null=True, blank=True)
    wifi_situation = models.IntegerField(choices=WIFI_CHOICES, default=None, null=True, blank=True)
    noise_level = models.IntegerField(choices=NOISE_CHOICES, default=None, null=True, blank=True)
    parking_situation = models.IntegerField(choices=PARKING_CHOICES, default=None, null=True, blank=True)

    location = models.ForeignKey(Location, on_delete=models.CASCADE) # location of the spot

    timestamp = models.DateTimeField(default=timezone.now) # time of the survey

    def get_busy_str(self):
        return dict(Survey.BUSY_CHOICES).get(self.busy_level)

    def get_comfort_str(self):
        return dict(Survey.COMFORT_CHOICES).get(self.comfort_level)

    def get_wifi_str(self):
        return dict(Survey.WIFI_CHOICES).get(self.wifi_situation)

    def get_noise_str(self):
        return dict(Survey.NOISE_CHOICES).get(self.noise_level)

    def get_parking_str(self):
        return dict(Survey.PARKING_CHOICES).get(self.parking_situation)

    def __str__(self):
        return f"Survey #{self.id}"

    @staticmethod
    def get_weighted_avg(location_id):
        # Get the location object based on the provided ID
        location = Location.objects.get(pk=location_id)

        # Get the current time, considering the timezone
        now = timezone.now()
        total_weight = 0

        # Initialize dictionary for storing weighted values
        weighted_values = {
            'busy_level': 0,
            'comfort_level': 0,
            'wifi_situation': 0,
            'noise_level': 0,
            'parking_situation': 0
        }

        # Iterate over each survey related to the specified location
        for survey in Survey.objects.filter(location=location):
            # Calculate the time difference in seconds and apply quadratic fall-off (square root)
            time_diff = max((now - survey.timestamp).total_seconds(), 1)  # Ensure at least 1 second to avoid division by zero
            weight = time_diff ** 0.5  # apply quadratic fall-off
            total_weight += weight

            # Aggregate the survey's weighted responses for each category
            for key in weighted_values:
                value = getattr(survey, key, None)
                if value is not None:
                    weighted_values[key] += value * weight

        # Normalize the aggregated values by dividing by the total weight (if greater than zero)
        if total_weight > 0:
            for key in weighted_values:
                weighted_values[key] /= total_weight

        return weighted_values
    

    @staticmethod
    def get_todays_avg(location_id):
        # Get today's date
        today = timezone.now().date()

        # Filter surveys for the given location and created today
        queryset = Survey.objects.filter(location_id=location_id, timestamp__date=today)

        # Aggregate and return averages
        return queryset.aggregate(
            Avg('busy_level'),
            Avg('comfort_level'),
            Avg('wifi_situation'),
            Avg('noise_level'),
            Avg('parking_situation')
        )
    
