from typing import Iterator
import grpc
from concurrent import futures

from spot.proto.spot_pb2 import LocationPan, LocationZoom, Parameter, QueryUpdate
from spot.proto.spot_pb2_grpc import LocationServiceServicer, add_LocationServiceServicer_to_server


class LocationServicer(LocationServiceServicer):
    lat = 0
    lon = 0
    radius = 0
    categories = {}
    attributes = {}


    def invalidate_cache(self):
        pass
        #check for each member in the cache if it is within the current radius, if not remove it


    def LocationSession(self, request_iterator: Iterator[QueryUpdate], context):
        # could be a sorted set of sorts
        cache = {} # max size 20
        for query_update in request_iterator:
            if query_update.HasField('pan'):
                yield from self.handle_pan(query_update.pan)
            elif query_update.HasField('zoom'):
                yield from self.handle_zoom(query_update.zoom)
            elif query_update.HasField('parameter'):
                yield from self.handle_param(query_update.parameter)

            self.invalidate_cache

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
