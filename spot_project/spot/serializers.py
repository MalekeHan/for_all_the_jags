from grpc import enum
from rest_framework import serializers
from django_grpc_framework import proto_serializers
import spot.proto.spot_pb2 as spot_pb2
"""
from models import MODEL
"""
from .models import Survey , Location

"""
Create the serializers for each model here
"""

##Serializer is used as a SERDE of the JSON data being sent to and from the SWIFT app to handle consistent dataflow
class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'  # Or list specific fields if needed

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'  # Serialize all fields from the Location model

class LocationPanProtoSerializer(proto_serializers.ProtoSerializer):
    lat = serializers.FloatField()
    lon = serializers.FloatField()

    class Meta:
        proto_class = spot_pb2.LocationPan

class LocationZoomProtoSerializer(proto_serializers.ProtoSerializer):
    radius = serializers.FloatField()

    class Meta:
        proto_class = spot_pb2.LocationZoom

class FilterType(enum.Enum):
    CATEGORY = 0
    ATTRIBUTES = 1

class ParameterProtoSerializer(proto_serializers.ProtoSerializer):
    type = serializers.ChoiceField(choices=FilterType, source='type', default=FilterType.CATEGORY)
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

class FlushSerializer(proto_serializers.ProtoSerializer):
    class Meta:
        proto_class = spot_pb2.Flush

class StreamUpdateProtoSerializer(proto_serializers.ProtoSerializer):
    location = LocationProtoSerializer()
    flush = FlushSerializer()

    class Meta:
        proto_class = spot_pb2.StreamUpdate

    def create(self, validated_data):
        if 'location' in validated_data:
            return spot_pb2.StreamUpdate(location=validated_data['location'])
        elif 'flush' in validated_data:
            return spot_pb2.StreamUpdate(flush=validated_data['flush'])
        else:
            raise serializers.ValidationError("Invalid data")
