from django.db import models

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
