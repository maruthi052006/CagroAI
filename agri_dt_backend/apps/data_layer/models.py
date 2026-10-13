from django.db import models

class Field(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    crop_type = models.CharField(max_length=50)
    owner = models.ForeignKey('accounts.FarmerProfile', on_delete=models.CASCADE, related_name='fields')

    def __str__(self):
        return f"{self.name} ({self.crop_type})"

class FieldRecord(models.Model):
    objects = models.Manager()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='records')
    date = models.DateField()
    temperature = models.FloatField(null=True, blank=True)
    rainfall = models.FloatField(null=True, blank=True)
    humidity = models.FloatField(null=True, blank=True)
    soil_moisture = models.FloatField(null=True, blank=True)
    pest_index = models.FloatField(null=True, blank=True)
    historical_yield = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Record for {self.field} on {self.date}"

class PredictionLog(models.Model):
    objects = models.Manager()
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='predictions')
    timestamp = models.DateTimeField(auto_now_add=True)
    output_data = models.JSONField() # Stores yield_mean, p10, p90, conflicts, etc.

    def __str__(self):
        return f"Prediction for {self.field} at {self.timestamp}"

