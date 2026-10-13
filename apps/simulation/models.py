from django.db import models

class FieldSimulationState(models.Model):
    field = models.OneToOneField('data_layer.Field', on_delete=models.CASCADE, related_name='simulation_state')
    growth_stage = models.FloatField(default=0.0)
    soil_moisture_pct = models.FloatField(default=50.0)
    pest_risk_pct = models.FloatField(default=0.0)
    weather_condition = models.CharField(max_length=50, default='clear')
    canopy_color_hex = models.CharField(max_length=7, default='#5FA052')
    crop_type = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)
