from django.db import models

class DecisionRecord(models.Model):
    class DecisionStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        MODIFIED = 'MODIFIED', 'Modified'

    field = models.ForeignKey('data_layer.Field', on_delete=models.CASCADE, related_name='decisions')
    prediction_log = models.ForeignKey('data_layer.PredictionLog', on_delete=models.SET_NULL, null=True, blank=True, related_name='decisions')
    recommendation_text = models.TextField()
    trust_score_at_time = models.FloatField(default=85.0)
    farmer_decision = models.CharField(max_length=20, choices=DecisionStatus.choices, default=DecisionStatus.PENDING)
    decision_reason = models.TextField(blank=True, default='')
    decided_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    decided_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Decision #{self.id} for Field {self.field_id}: {self.farmer_decision}"


class OutcomeRecord(models.Model):
    field = models.ForeignKey('data_layer.Field', on_delete=models.CASCADE, related_name='outcomes')
    decision_record = models.ForeignKey(DecisionRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='outcomes')
    predicted_yield = models.FloatField()
    actual_yield = models.FloatField()
    prediction_error_pct = models.FloatField(null=True, blank=True)
    season_year = models.IntegerField(default=2026)
    notes = models.TextField(blank=True, default='')
    recorded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.actual_yield and self.actual_yield > 0:
            self.prediction_error_pct = round(abs(self.actual_yield - self.predicted_yield) / self.actual_yield * 100.0, 2)
        else:
            self.prediction_error_pct = 0.0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Outcome for Field {self.field_id}: Actual={self.actual_yield} vs Pred={self.predicted_yield} (Error: {self.prediction_error_pct}%)"
