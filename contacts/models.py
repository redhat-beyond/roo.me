from django.db import models
from datetime import date
from users.models import Apartment, Seeker


class Connection(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='apt_connection')
    seeker = models.ForeignKey(Seeker, on_delete=models.CASCADE, related_name='seeker_connection')
    date_created = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.apartment.owner.first_name} and {self.seeker.base_user.first_name}'s connection"

    class Meta:
        unique_together = ['apartment', 'seeker']
