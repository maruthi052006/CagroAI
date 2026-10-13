import os

project_dir = "c:/Users/Sathiyabhama/OneDrive/Desktop/digital twin project/agri_dt_backend"

def write_model(app, content):
    with open(f"{project_dir}/apps/{app}/models.py", "w") as f:
        f.write(content)

# apps/zones/models.py
zones_content = """from django.db import models

class Zone(models.Model):
    REGION_CHOICES = [
        ('NORTHERN', 'Northern'),
        ('WESTERN', 'Western'),
        ('SOUTHERN', 'Southern'),
        ('CENTRAL', 'Central'),
        ('DELTA', 'Delta'),
    ]
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20)
    region_group = models.CharField(max_length=20, choices=REGION_CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
"""
write_model("zones", zones_content)

# apps/accounts/models.py
accounts_content = """from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        OFFICER = 'OFFICER', 'Agri Officer'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)

class OfficerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    zones = models.ManyToManyField('zones.Zone', related_name='officers')

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    zone = models.ForeignKey('zones.Zone', on_delete=models.RESTRICT)
    assigned_officer = models.ForeignKey(OfficerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_farmers')
    needs_officer_assignment = models.BooleanField(default=False)
"""
write_model("accounts", accounts_content)

# apps/data_layer/models.py
data_layer_content = """from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    crop_type = models.CharField(max_length=50)
    owner = models.ForeignKey('accounts.FarmerProfile', on_delete=models.CASCADE, related_name='fields')

class FieldRecord(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    temperature = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    soil_moisture = models.FloatField(null=True, blank=True)
    pest_index = models.FloatField(null=True, blank=True)
    historical_yield = models.FloatField(null=True, blank=True)

class PredictionLog(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='predictions')
    timestamp = models.DateTimeField(auto_now_add=True)
    output_data = models.JSONField() # Stores yield_mean, p10, p90, conflicts, etc.
"""
write_model("data_layer", data_layer_content)

# apps/simulation/models.py
simulation_content = """from django.db import models

class FieldSimulationState(models.Model):
    field = models.OneToOneField('data_layer.Field', on_delete=models.CASCADE, related_name='simulation_state')
    growth_stage = models.FloatField(default=0.0)
    soil_moisture_pct = models.FloatField(default=50.0)
    pest_risk_pct = models.FloatField(default=0.0)
    weather_condition = models.CharField(max_length=50, default='clear')
    canopy_color_hex = models.CharField(max_length=7, default='#5FA052')
    crop_type = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)
"""
write_model("simulation", simulation_content)

# apps/alerts/models.py
alerts_content = """from django.db import models

class Alert(models.Model):
    sender = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_alerts')
    recipient = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='alerts')
    field = models.ForeignKey('data_layer.Field', on_delete=models.CASCADE, null=True, blank=True)
    alert_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
"""
write_model("alerts", alerts_content)

# apps/messaging/models.py
messaging_content = """from django.db import models

class Conversation(models.Model):
    farmer = models.ForeignKey('accounts.FarmerProfile', on_delete=models.CASCADE)
    officer = models.ForeignKey('accounts.OfficerProfile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=20, default='text') # text, image, document, video, voice
    text_content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='messages/attachments/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='messages/thumbnails/', null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, default='sent')
    sent_at = models.DateTimeField(auto_now_add=True)
"""
write_model("messaging", messaging_content)

print("Models written successfully.")
