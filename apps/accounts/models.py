from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        FARMER = 'FARMER', 'Farmer'
        OFFICER = 'OFFICER', 'Agri Officer'
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.FARMER)

class OfficerProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='officer_profile')
    zones = models.ManyToManyField('zones.Zone', related_name='officers')

    def __str__(self):
        return f"OfficerProfile for {self.user.username}"

class FarmerProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    zone = models.ForeignKey('zones.Zone', on_delete=models.RESTRICT)
    assigned_officer = models.ForeignKey(OfficerProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_farmers')
    needs_officer_assignment = models.BooleanField(default=False)

    def __str__(self):
        return f"FarmerProfile for {self.user.username}"

