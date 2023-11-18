from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
import logging

from rest_framework.views import APIView, Response

from spot.yelp import YelpHandler

"""
from models import MODELS
from serializers import SERIALIZERS
"""
# Create your views here.

logger = logging.getLogger(__name__)

class SearchView(APIView):
    def get(self, request: HttpRequest):
        logger.info("SearchView.get")
        params = request.query_params
        res = YelpHandler.search(params)
        businesses = res.get("businesses", [])
        return Response(businesses)





