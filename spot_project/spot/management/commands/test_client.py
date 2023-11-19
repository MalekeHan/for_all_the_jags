from django.core.management.base import BaseCommand

from spot import test_client

class Command(BaseCommand):
    help = 'Starts the gRPC client'

    def handle(self, *args, **options):
        self.stdout.write('Starting gRPC server...')
        test_client.run()
