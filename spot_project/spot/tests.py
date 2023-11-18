from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Survey, Location


# Create your tests here.
class ModelTests(TestCase):

    def setUp(self):
        self.location = Location.objects.create(name='Test Location', address='123 Test St')

    def test_create_location(self):
        """Test creating a location is successful"""
        self.assertEqual(self.location.name, 'Test Location')
        self.assertEqual(self.location.address, '123 Test St')

    def test_create_survey(self):
        """Test creating a survey with valid data is successful"""
        survey = Survey.objects.create(
            busy_level=2,  # using integers as per the new model definition
            comfort_level=2,
            wifi_situation=2,
            noise_level=2,
            parking_situation=2,
            location=self.location
        )
        self.assertEqual(survey.busy_level, 2)
        self.assertEqual(survey.location, self.location)
    
    def test_get_busy_str(self):
        """Test the get_busy_str method returns correct string"""
        survey = Survey.objects.create(busy_level=0, location=self.location)
        self.assertEqual(survey.get_busy_str(), 'Very busy')

from django.db.models import Avg
from datetime import datetime, timedelta
from django.utils import timezone

class SurveyAggregateViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.location = Location.objects.create(name='Test Location', address='123 Test St')

        # Create surveys with different timestamps
        Survey.objects.create(
            busy_level=2,
            comfort_level=2,
            wifi_situation=2,
            noise_level=2,
            parking_situation=2,
            location=self.location,
            timestamp=timezone.now()  # Survey created today
        )

        Survey.objects.create(
            busy_level=1,
            comfort_level=1,
            wifi_situation=1,
            noise_level=1,
            parking_situation=1,
            location=self.location,
            timestamp=timezone.now() - timedelta(days=30)  # Survey created last month
        )

        self.surveys_url = reverse('survey-aggregate')  # Ensure this URL name matches your URL configuration

    def test_aggregate_data(self):
        """Test retrieving aggregated survey data"""
        response = self.client.get(self.surveys_url, {'location_id': self.location.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Here, you should compare response.data with the expected aggregated data
        # Since you're using a custom aggregation method, you may need to calculate the expected results manually or use the same method in the test
        aggregated_data = Survey.get_weighted_avg(self.location.id)
        self.assertAlmostEqual(response.data['busy_level'], aggregated_data['busy_level'])

    def test_get_todays_avg(self):
        # Call get_todays_avg and verify the results
        todays_avg = Survey.get_todays_avg(self.location.id)

        # Expected averages should be based on surveys created today only
        expected_busy_avg = 2  # As there's only one survey today with busy_level = 2
        expected_comfort_avg = 2
        expected_wifi_avg = 2
        expected_noise_avg = 2
        expected_parking_avg = 2

        self.assertAlmostEqual(todays_avg['busy_level__avg'], expected_busy_avg)
        self.assertAlmostEqual(todays_avg['comfort_level__avg'], expected_comfort_avg)
        self.assertAlmostEqual(todays_avg['wifi_situation__avg'], expected_wifi_avg)
        self.assertAlmostEqual(todays_avg['noise_level__avg'], expected_noise_avg)
        self.assertAlmostEqual(todays_avg['parking_situation__avg'], expected_parking_avg)



