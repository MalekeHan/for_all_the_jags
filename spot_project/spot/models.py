from datetime import datetime
from django.db import models
from django.db.models.aggregates import Avg

# Create your models here.

## Location of the Spot
class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

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
    busy_level = models.IntegerField(choices=BUSY_CHOICES, default=None)
    busy_str = models.CharField(choices=BUSY_CHOICES, default=None)

    comfort_level = models.IntegerField(choices=COMFORT_CHOICES, default=None)
    comfort_str = models.CharField(choices=COMFORT_CHOICES, default=None)

    wifi_situation = models.IntegerField(choices=WIFI_CHOICES, default=None)
    wifi_str = models.CharField(choices=WIFI_CHOICES, default=None)
    
    noise_level = models.IntegerField(choices=NOISE_CHOICES, default=None)
    noise_str = models.CharField(choices=NOISE_CHOICES, default=None)

    parking_situation = models.IntegerField(choices=PARKING_CHOICES, default=None)
    parking_str = models.CharField(choices=PARKING_CHOICES, default=None)

    location = models.ForeignKey(Location, on_delete=models.CASCADE) # location of the spot

    timestamp = models.DateTimeField(auto_now_add=True) # time of the survey

    def __str__(self):
        return f"Survey #{self.id}"

    @staticmethod
    def get_weighted_avg(location_id):
        # Get all objects for the given location
        location = Location.objects.get(pk=location_id)
        queryset = Survey.objects.filter(location=location)

        # Calculate weights based on timestamp
        now = datetime.now()
        queryset = queryset.annotate(
            time_diff=models.F('timestamp') - now,
            weight=models.Func(
                # Square root to introduce quadratic fall-off (i.e. more recent surveys are weighted more heavily)
                models.F('time_diff'),
                function='POW',
                template='SQRT(EXTRACT(EPOCH FROM %s))',  

            ),
        )

        # Calculate the total weight (sum of all weights)
        total_weight = sum(entry.weight for entry in queryset)

        # Calculate weighted averages for each field
        busy_avg = sum(entry.busy_level * (entry.weight / total_weight) for entry in queryset)
        comfort_avg = sum(entry.comfort_level * (entry.weight / total_weight) for entry in queryset)
        wifi_avg = sum(entry.wifi_situation * (entry.weight / total_weight) for entry in queryset)
        noise_avg = sum(entry.noise_level * (entry.weight / total_weight) for entry in queryset)
        parking_avg = sum(entry.parking_situation * (entry.weight / total_weight) for entry in queryset)

        return {
            'busy_level': busy_avg,
            'comfort_level': comfort_avg,
            'wifi_situation': wifi_avg,
            'noise_level': noise_avg,
            'parking_situation': parking_avg,
        }

    @staticmethod
    def get_todays_avg(location_id):
        # get today's objects
        queryset = Survey.objects.filter(survey_date=datetime.date.today())

        location = Location.objects.get(pk=location_id)
        queryset = queryset.filter(location=location)

        return queryset.aggregate(
            Avg('busy_level'),
            Avg('comfort_level'),
            Avg('wifi_situation'),
            Avg('noise_level'),
            Avg('parking_situation')
        )
    
