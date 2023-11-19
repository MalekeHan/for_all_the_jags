from typing import Iterator 
import grpc
from concurrent import futures

from spot.proto.spot_pb2 import Parameter, QueryUpdate
from spot.proto.spot_pb2_grpc import LocationServiceServicer, add_LocationServiceServicer_to_server
from spot.models import Survey
from spot.models import Location
from spot.yelp import YelpHandler
from geopy.distance import geodesic

class SessionState:
    lat = 0.0
    lon = 0.0
    radius = 5000
    categories = set()
    attributes = set()

    def __init__(self, max_size=20):
        self.max_size = max_size
        self.locations = []

    def add_location(self, location: Location):
        # Calculate the aggregated score for the location
        aggregated_score = Survey.get_weighted_avg(location.id)
        total_score = self.calculate_total_score(aggregated_score)

        location_with_score = {
            'location': location,
            'score': total_score
        }

        # Add location to cache and maintain sorting based on score
        self.locations.append(location_with_score)
        self.locations.sort(key=lambda loc: loc['score'], reverse=True)
        self.invalidate_cache()
        self._trim_cache()
    
    def _trim_cache(self):
        if len(self.locations) > self.max_size:
            self.locations = self.locations[:self.max_size]

    def calculate_total_score(self, aggregated_values):
        return sum(aggregated_values.values())

    def remove_locations_outside_radius(self, center_lat, center_lon, radius):
        self.locations = [
            loc for loc in self.locations 
            if self.is_within_radius(loc['location'], center_lat, center_lon, radius)
        ]

    # distance between the location and the center point
    @staticmethod
    def is_within_radius(location, center_lat, center_lon, radius):
        return SessionState.calculate_distance(location.lat, location.lon, center_lat, center_lon) <= radius

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        distance = geodesic((lat1, lon1), (lat2, lon2)).meters
        return distance

    def invalidate_cache(self):
        # Check for each location in the cache if it is within the current radius
        if self.radius > 0:
            self.remove_locations_outside_radius(self.lat, self.lon, self.radius)


class LocationServicer(LocationServiceServicer):
    def LocationSession(self, request_iterator: Iterator[QueryUpdate], context):
        print("LocationSession started")
        state = SessionState() 
        for query_update in request_iterator:
            print("Received query update")
            if query_update.HasField('pan'):
                print("Received pan update")
                state.lat = query_update.pan.lat
                state.lon = query_update.pan.lon
            elif query_update.HasField('zoom'):
                print("Received zoom update")
                state.radius = query_update.zoom.radius
            elif query_update.HasField('parameter'):
                print("Received parameter update")
                ref = state.categories if query_update.parameter.type == Parameter.type.CATEGORY else state.attributes
                if query_update.parameter.add:
                    ref.add(query_update.parameter.value)
                else:
                    ref.remove(query_update.parameter.value)
            else:
                print("Received unknown update")
                continue

            state.invalidate_cache()

            locs = state.locations
            print("state.locs", locs)
            yield from locs
            locs = self.search_yelp(state)
            locs = state.locations
            print("state.locs", locs)

    @staticmethod
    def search_yelp(state: SessionState):
        """Searches yelp for locations based on the current state of the session. Returns a generator of locations."""

        builder = YelpHandler.QueryBuilder()
        builder.latitude(state.lat)
        builder.longitude(state.lon)
        builder.radius(state.radius)
        builder.categories(state.categories)
        builder.attributes(state.attributes)
        params = builder.build()

        businesses = YelpHandler.search(params)
        for business in businesses:
            print("Found business: " + business.name)
            location = Location.objects.get_or_create(
                name=business.name,
                lat=business.latitude,
                lon=business.longitude,
                yelp_id=business.id
            )
            state.add_location(location)
            print(location)
            yield location


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LocationServiceServicer_to_server(LocationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
