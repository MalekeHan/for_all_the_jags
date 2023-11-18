from rest_framework import serializers

"""
from models import MODEL
"""
from .models import Survey

"""
Create the serializers for each model here
"""

##Serializer is used as a SERDE of the JSON data being sent to and from the SWIFT app to handle consistent dataflow
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'  # Or list specific fields if needed
