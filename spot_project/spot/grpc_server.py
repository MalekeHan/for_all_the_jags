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

    # could be a sorted set of sorts
    cache = {}

    def LocationSession(self, request_iterator: Iterator[QueryUpdate], context):
        for query_update in request_iterator:
            if query_update.HasField('pan'):
                yield from self.handle_pan(query_update.pan)
            elif query_update.HasField('zoom'):
                yield from self.handle_zoom(query_update.zoom)
            elif query_update.HasField('parameter'):
                yield from self.handle_param(query_update.parameter)

    def handle_pan(self, pan: LocationPan):
        # todo
        pass

    def handle_zoom(self, zoom: LocationZoom):
        # todo
        pass

    def handle_param(self, param: Parameter):
        # todo
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_LocationServiceServicer_to_server(LocationServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
