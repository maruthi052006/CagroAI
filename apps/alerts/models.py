from django.db import models

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
