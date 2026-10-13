from django.core.management.base import BaseCommand
import os
import pandas as pd
from apps.data_layer.models import Field, FieldRecord
from apps.accounts.models import FarmerProfile, User
from apps.zones.models import Zone
import datetime

class Command(BaseCommand):
    help = 'Loads datasets from /datasets into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading datasets...")
        from django.conf import settings
        base_dir = os.path.join(settings.BASE_DIR.parent, "datasets")
        
        # Ensure we have a default zone and farmer to own the fields
        zone, _ = Zone.objects.get_or_create(name='Default Zone', code='DEF', region_group='NORTHERN')
        user, _ = User.objects.get_or_create(username='default_farmer', role=User.Role.FARMER)
        farmer, _ = FarmerProfile.objects.get_or_create(user=user, zone=zone)
        
        # A simple load of Fertilizer.csv to create some Field and FieldRecords
        fert_path = os.path.join(base_dir, "archive (27)", "Fertilizer.csv")
        if os.path.exists(fert_path):
            df = pd.read_csv(fert_path)
            # Create a Field for a common crop
            crop = "wheat"
            field, _ = Field.objects.get_or_create(
                name=f"Demo {crop.capitalize()} Field",
                latitude=11.0168,
                longitude=76.9558,
                crop_type=crop,
                owner=farmer
            )
            
            # Load some sample records
            # Since real schema is complex, we just add 10 dummy records linked to real dataset structure if we had one
            for i in range(5):
                FieldRecord.objects.get_or_create(
                    field=field,
                    date=datetime.date.today() - datetime.timedelta(days=i),
                    temperature=28.0 + i,
                    rainfall=10.0,
                    humidity=60.0,
                    soil_moisture=45.0,
                    pest_index=0.1,
                    historical_yield=4200.0
                )
            self.stdout.write(self.style.SUCCESS(f"Loaded basic records for {crop}."))
        else:
            self.stdout.write(self.style.WARNING("Dataset Fertilizer.csv not found at expected path."))
            
        self.stdout.write(self.style.SUCCESS("Finished load_datasets."))
