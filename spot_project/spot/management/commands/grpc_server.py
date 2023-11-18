from django.core.management.base import BaseCommand
from ... import grpc_server

class Command(BaseCommand):
    help = 'Starts the gRPC server'

    def handle(self, *args, **options):
        self.stdout.write('Starting gRPC server...')
        grpc_server.serve()
