from typing import Iterator
import grpc
from concurrent import futures

from spot.proto.spot_pb2 import LocationPan, LocationZoom, Parameter, QueryUpdate
from spot.proto.spot_pb2_grpc import LocationServiceServicer, add_LocationServiceServicer_to_server
from spot.models import Survey
from spot.models import Location

class Cache:
    def __init__(self, max_size=20):
        self.max_size = max_size
        self.locations = []

    def add_location(self, location_id):
        # Calculate the aggregated score for the location
        aggregated_score = Survey.get_weighted_avg(location_id)
        total_score = self.calculate_total_score(aggregated_score)

        location = Location.objects.get(pk=location_id)
        location_with_score = {
            'location': location,
            'score': total_score
        }

        # Add location to cache and maintain sorting based on score
        self.locations.append(location_with_score)
        self.locations.sort(key=lambda loc: loc['score'], reverse=True)
        self._trim_cache()

    def calculate_total_score(self, aggregated_values):
        return sum(aggregated_values.values())

    def remove_locations_outside_radius(self, center_lat, center_lon, radius):

        # we still need to write to the DB here

        self.locations = [
            loc for loc in self.locations 
            if self.is_within_radius(loc['location'], center_lat, center_lon, radius)
        ]

    # distance between the location and the center point
    @staticmethod
    def is_within_radius(location, center_lat, center_lon, radius):
        return Cache.calculate_distance(location.lat, location.lon, center_lat, center_lon) <= radius

    def calculate_distance(lat1, lon1, lat2, lon2):
        pass # i dont know if this is needed tbh


class LocationServicer(LocationServiceServicer):
    lat = 0
    lon = 0
    radius = 0
    categories = {}
    attributes = {}


    def invalidate_cache(self, cache: Cache):
        # Check for each location in the cache if it is within the current radius
        if self.radius > 0:
            cache.remove_locations_outside_radius(self.lat, self.lon, self.radius)


    def LocationSession(self, request_iterator: Iterator[QueryUpdate], context):
        # could be a sorted set of sorts
        cache = Cache() 
        for query_update in request_iterator:
            if query_update.HasField('pan'):
                yield from self.handle_pan(query_update.pan)
            elif query_update.HasField('zoom'):
                yield from self.handle_zoom(query_update.zoom)
            elif query_update.HasField('parameter'):
                yield from self.handle_param(query_update.parameter)

            self.invalidate_cache(cache)

    def handle_pan(self, pan: LocationPan):
        # todo
        self.lat = pan.lat
        self.lon = pan.lon
        pass

    def handle_zoom(self, zoom: LocationZoom):
        # todo
        self.radius = zoom.radius
        pass

    def handle_param(self, param: Parameter):
        # todo
        if param.type == param.type.CATEGORY:
            self.categories[param.value] = param.add
        elif param.type == param.type.ATTRIBUTES:
            self.attributes[param.value] = param.add
            
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LocationServiceServicer_to_server(LocationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
