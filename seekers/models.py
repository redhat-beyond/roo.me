from django.db import models
from roo_me.settings import AUTH_USER_MODEL


class Seeker(models.Model):
    base_user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    city = models.ForeignKey('apartments.City', on_delete=models.RESTRICT, related_name='city_seekers')
    start_date = models.DateField()
    min_rent = models.IntegerField()
    max_rent = models.IntegerField()
    num_of_roomates = models.IntegerField()
    num_of_rooms = models.IntegerField()
    about = models.TextField(blank=True)

    def __str__(self):
        return f"Seeker:{self.base_user}"
