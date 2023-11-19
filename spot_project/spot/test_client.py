# from typing import Iterator
# import grpc

# from spot.proto import spot_pb2, spot_pb2_grpc

# def get_random_location():
#     query_update = spot_pb2.QueryUpdate(
#             pan=spot_pb2.LocationPan(
#             lat=37.773972,
#             lon=-122.431297,
#         )
#     )
#     return query_update

# def generate_locations():
#     for _ in range(1):
#         yield get_random_location()

# def run():
#     with grpc.insecure_channel("localhost:50051") as channel:
#         stub = spot_pb2_grpc.LocationServiceStub(channel)
#         stream_updates: Iterator[spot_pb2.StreamUpdate] = stub.LocationSession(generate_locations())
#         for stream_update in stream_updates:
#             print(stream_update)

# if __name__ == "__main__":
#     run()

import grpc
from spot.proto import spot_pb2, spot_pb2_grpc

def get_location_update(lat, lon):
    return spot_pb2.QueryUpdate(
        pan=spot_pb2.LocationPan(lat=lat, lon=lon)
    )

def run(lat, lon):
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = spot_pb2_grpc.LocationServiceStub(channel)
        query_update = get_location_update(lat, lon)
        stream_updates = stub.LocationSession(iter([query_update]))
        for stream_update in stream_updates:
            print(stream_update)

if __name__ == "__main__":
    # Example usage with a specific latitude and longitude
    run(37.773972, -122.431297)