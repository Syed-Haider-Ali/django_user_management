import os
import json
from django.core.management.base import BaseCommand
from user_auth.models import User
from user_auth.user_serializer import UserSerializer  

class Command(BaseCommand):
    help = 'Export data from default database to JSON file'

    def handle(self, *args, **options):
        # Query data from the default database
        data = User.objects.all()

        # Serialize the data
        serialized_data = UserSerializer(data, many=True).data  # Use your serializer if needed

        # Define the path for the JSON file
        output_file = 'data_export.json'

        # Write data to JSON file
        with open(output_file, 'w') as f:
            json.dump(serialized_data, f, indent=4)

        self.stdout.write(self.style.SUCCESS(f'Successfully exported data to {output_file}'))
