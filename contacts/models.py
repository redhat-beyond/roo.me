from django.db import models
from datetime import date
from django.utils import timezone
from users.models import User
from django.core.exceptions import ObjectDoesNotExist


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
        if(self.status != ConnectionType.PENDING):
            raise ValueError('Connection cannot be approved!')
        else:
            self.status = ConnectionType.APPROVED
            self.save()

    def reject(self):
        self.status = ConnectionType.REJECTED
        self.save()

    def get_chat_messages(self):
        return self.messages.all()

    @property
    def get_status(self):
        return self.status.label

    @classmethod
    def get_connection_by_id(cls, con_id):
        try:
            return cls.objects.get(id=con_id)
        except ObjectDoesNotExist:
            return None

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


class Message(models.Model):
    connection = models.ForeignKey(Connection, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='user_messages', on_delete=models.CASCADE)
    text = models.TextField(max_length=300)
    date_written = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text
