from rest_framework import serializers

"""
from models import MODEL
"""
from .models import Survey

"""
Create the serializers for each model here
"""

##Serializer is used to 
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'  # Or list specific fields if needed