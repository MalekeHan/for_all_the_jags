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
from rest_framework import status
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
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            location_id = serializer.data.get('location')
            if location_id:
                Survey.get_weighted_avg(location_id)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SurveyAggregateView(APIView):
    def get(self, request, format=None):
        location_id = request.query_params.get('location_id', None)
        if not location_id:
            return Response({"error": "Location ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        aggregated_data = Survey.get_weighted_avg(location_id)

        return Response(aggregated_data)

