from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
import logging

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView, Response

from spot.yelp import YelpHandler

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




