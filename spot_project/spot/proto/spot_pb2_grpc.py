# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import spot_pb2 as spot__pb2


class LocationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LocationSession = channel.stream_stream(
                '/LocationService/LocationSession',
                request_serializer=spot__pb2.QueryUpdate.SerializeToString,
                response_deserializer=spot__pb2.StreamUpdate.FromString,
                )


class LocationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LocationSession(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LocationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LocationSession': grpc.stream_stream_rpc_method_handler(
                    servicer.LocationSession,
                    request_deserializer=spot__pb2.QueryUpdate.FromString,
                    response_serializer=spot__pb2.StreamUpdate.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LocationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LocationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LocationSession(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/LocationService/LocationSession',
            spot__pb2.QueryUpdate.SerializeToString,
            spot__pb2.StreamUpdate.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
