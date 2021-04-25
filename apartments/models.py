from django.db import models
from django.utils import timezone
from roo_me.settings import AUTH_USER_MODEL


class City(models.Model):
    cityName = models.CharField(max_length=100)

    def __str__(self):
        return self.cityName


class Apartment(models.Model):
    owner = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    date_posted = models.DateTimeField(default=timezone.now, blank=True)
    city = models.ForeignKey(City, on_delete=models.RESTRICT, related_name='city_apartments')
    address = models.TextField()
    rent = models.IntegerField()
    num_of_roomates = models.IntegerField()
    num_of_rooms = models.IntegerField()
    start_date = models.DateField()
    about = models.TextField(blank=True)
    is_relevant = models.BooleanField(default=True, blank=True)
    image_url = models.TextField(blank=True)

    def __str__(self):
        return f"Owner:{self.owner}, Addres:{self.address}, City:{self.city}"
