from rest_framework import serializers
from django_grpc_framework import proto_serializers
import spot.proto.spot_pb2 as spot_pb2
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

class LocationPanProtoSerializer(proto_serializers.ProtoSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

    class Meta:
        proto_class = spot_pb2.LocationPan

class LocationZoomProtoSerializer(proto_serializers.ProtoSerializer):
    radius = serializers.FloatField()

    class Meta:
        proto_class = spot_pb2.LocationZoom

class ParameterProtoSerializer(proto_serializers.ProtoSerializer):
    type = serializers.ChoiceField(choices=spot_pb2.FilterType.values)
    value = serializers.CharField(max_length=100)
    add = serializers.BooleanField()

    class Meta:
        proto_class = spot_pb2.Parameter

class LocationProtoSerializer(proto_serializers.ProtoSerializer):
    id = serializers.CharField(max_length=100)
    lat = serializers.FloatField()
    lon = serializers.FloatField()
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    attributes = serializers.CharField(max_length=100)

    class Meta:
        proto_class = spot_pb2.Location

class QueryUpdateProtoSerializer(proto_serializers.ProtoSerializer):
    pan = LocationPanProtoSerializer()
    zoom = LocationZoomProtoSerializer()
    parameter = ParameterProtoSerializer()

    class Meta:
        proto_class = spot_pb2.QueryUpdate

    def create(self, validated_data):
        if 'pan' in validated_data: # we need to worry about the one of so conditionally check here
            return spot_pb2.QueryUpdate(pan=validated_data['pan'])
        elif 'zoom' in validated_data:
            return spot_pb2.QueryUpdate(zoom=validated_data['zoom'])
        elif 'parameter' in validated_data:
            return spot_pb2.QueryUpdate(parameter=validated_data['parameter'])
        else:
            raise serializers.ValidationError("Invalid data")
