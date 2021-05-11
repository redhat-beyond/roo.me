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
            self.save()

    def reject(self):
        self.status = ConnectionType.REJECTED
        self.save()

    @property
    def get_status(self):
        return self.status.label

    @classmethod
    def get_connections_by_user(cls, user, desired_status):
        if user.is_seeker:
            seeker_profile = user.seeker
            connections = cls.objects.filter(seeker=seeker_profile, status=desired_status)
        else:
            apartment_profile = user.apartment
            connections = cls.objects.filter(apartment=apartment_profile, status=desired_status)

        return connections

    class Meta:
        unique_together = ['apartment', 'seeker']
