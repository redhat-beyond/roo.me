from django.db import models
from datetime import date


class ConnectionType(models.TextChoices):
    PENDING = 'P', 'Pending'
    APPROVED = 'A', 'Approved'
    REJECTED = 'R', 'Rejected'


class Connection(models.Model):
    apartment = models.ForeignKey('apartments.Apartment', on_delete=models.CASCADE, related_name='apt_connection')
    seeker = models.ForeignKey('seekers.Seeker', on_delete=models.CASCADE, related_name='seeker_connection')
    status = models.CharField(
        max_length=1,
        choices=ConnectionType.choices,
        default=ConnectionType.PENDING
    )
    date_created = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.apartment.owner.first_name} and {self.seeker.base_user.first_name}'s connection"

    def approve(self):
        if(self.status is not ConnectionType.PENDING):
            raise ValueError('Connection cannot be approved!')
        else:
            self.status = ConnectionType.APPROVED

    def reject(self):
        self.status = ConnectionType.REJECTED

    @property
    def get_status(self):
        return self.status.label

    class Meta:
        unique_together = ['apartment', 'seeker']
