from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView, Response
from spot.yelp import YelpHandler

from .models import Survey
from .serializers import SurveySerializer

"""
from models import MODELS
from serializers import SERIALIZERS
"""
# Create your views here.

logger = logging.getLogger(__name__)

# class SearchView(APIView):
#     def get(self, request: HttpRequest):
#         logger.info("SearchView.get")
#         params = request.query_params
#         res = YelpHandler.search(params)
#         businesses = res.get("businesses", [])
#         return Response(businesses)

class SearchViewSet(ViewSet):
    def list(self, request):
        logger.info("SearchViewSet.list")
        params = request.query_params
        res = YelpHandler.search(params)
        businesses = res.get("businesses", [])
        return Response(businesses)
    
class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def create(self, request, *args, **kwargs):
        # Add custom logic for POST request if necessary
        return super().create(request, *args, **kwargs)


class SurveyAggregateView(APIView):
    def get(self, request, format=None):
        location_id = request.query_params.get('location_id', None)
        if not location_id:
            return Response({"error": "Location ID is required"}, status=status.HTTP_400_BAD_REQUEST)


        choice_to_numeric = {'NB': 1, 'MB': 2, 'VB': 3, 'VC': 1, 'MC': 2, 'NC': 3, # we need to map each of the "responses" from the survey to a numeric val -- could've maybe just stored em as nums in the first place smh
                             'NW': 1, 'PW': 2, 'FW': 3, 'QZ': 1, 'MN': 2, 'VN': 3,
                             'EP': 1, 'MP': 2, 'DP': 3}


        survey_data = Survey.objects.filter(location_id=location_id) #by location we can get the summation of the "total" from the responses and then divide by the amount of surveys we have for that location
        aggregated_data = {
            'average_busy_level': sum(choice_to_numeric[s.busy_level] for s in survey_data) / survey_data.count(),
            'average_comfort_level': sum(choice_to_numeric[s.comfort_level] for s in survey_data) / survey_data.count(),
            'average_wifi_situation': sum(choice_to_numeric[s.wifi_situation] for s in survey_data) / survey_data.count(),
            'average_noise_level': sum(choice_to_numeric[s.noise_level] for s in survey_data) / survey_data.count(),
            'average_parking_situation': sum(choice_to_numeric[s.parking_situation] for s in survey_data) / survey_data.count(),
        }

        return Response(aggregated_data)

