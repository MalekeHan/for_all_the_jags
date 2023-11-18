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
            busy_level='NB',
            comfort_level='VC',
            wifi_situation='NW',
            noise_level='QZ',
            parking_situation='EP',
            location=self.location
        )
        self.assertEqual(survey.busy_level, 'NB')
        self.assertEqual(survey.location, self.location)

from django.db.models import Avg

class SurveyAggregateViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.location = Location.objects.create(name='Test Location', address='123 Test St')

        # create surveys
        Survey.objects.create(busy_level='NB', comfort_level='VC', wifi_situation='NW', noise_level='QZ', parking_situation='EP', location=self.location)
        Survey.objects.create(busy_level='MB', comfort_level='MC', wifi_situation='PW', noise_level='MN', parking_situation='MP', location=self.location)
        self.surveys_url = reverse('survey-aggregate') #dynamically generate the URL for the view --Django will go and look up this name in our urls and find the url path "/aggregate"

    def test_aggregate_data(self):
        """Test retrieving aggregated survey data"""
        response = self.client.get(self.surveys_url, {'location_id': self.location.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # have to manually assign the numerical vals to calc averages here
        surveys = Survey.objects.filter(location=self.location) 
        total_busy_level = sum(1 if s.busy_level == 'NB' else 2 if s.busy_level == 'MB' else 3 for s in surveys)
        average_busy_level = total_busy_level / surveys.count() if surveys.count() > 0 else 0

        total_comfort_level = sum(1 if s.comfort_level == 'VC' else 2 if s.comfort_level == 'MC' else 3 for s in surveys)
        average_comfort_level = total_comfort_level / surveys.count() if surveys.count() > 0 else 0

        # check assertions
        self.assertAlmostEqual(response.data['average_busy_level'], average_busy_level)
        self.assertAlmostEqual(response.data['average_comfort_level'], average_comfort_level)




