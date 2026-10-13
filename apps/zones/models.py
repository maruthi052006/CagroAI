from django.db import models

class Zone(models.Model):
    objects = models.Manager()
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

    def __str__(self) -> str:
        return str(self.name)


