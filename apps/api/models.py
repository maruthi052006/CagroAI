from django.db import models

class MLModelVersion(models.Model):
    agent_name = models.CharField(max_length=100)
    version = models.CharField(max_length=50)
    algorithm_description = models.TextField()
    metrics = models.JSONField() # real computed RMSE, MAE, R2, etc.
    trained_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.agent_name} v{self.version}"
