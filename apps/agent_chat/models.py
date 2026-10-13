from django.db import models

class Persona(models.TextChoices):
    CROP = 'CROP', 'Crop Growth Agent'
    WEATHER = 'WEATHER', 'Weather Agent'
    PEST = 'PEST', 'Pest & Disease Agent'
    YIELD = 'YIELD', 'Yield Forecast Agent'
    EXAI = 'EXAI', 'Explainable AI (EXAI)'

class AgentConversation(models.Model):
    objects = models.Manager()
    field = models.ForeignKey('data_layer.Field', on_delete=models.CASCADE, related_name='agent_conversations')
    persona = models.CharField(max_length=20, choices=Persona.choices, default=Persona.EXAI)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        f_id = getattr(self, 'field_id', None) or getattr(self, 'pk', 'unknown')
        return f"{self.persona} chat for Field #{f_id}"

class AgentChatMessage(models.Model):
    class SenderRole(models.TextChoices):
        USER = 'USER', 'User'
        AGENT = 'AGENT', 'Agent'

    objects = models.Manager()
    conversation = models.ForeignKey(AgentConversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SenderRole.choices, default=SenderRole.USER)
    intent_detected = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField()
    data_sources_used = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        content = str(getattr(self, 'text', '') or '')
        return f"[{self.sender}][{self.intent_detected}] {content[:40]}"

