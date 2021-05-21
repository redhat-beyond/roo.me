from django.db import models
from django.utils import timezone
from roo_me.settings import AUTH_USER_MODEL
from django.core.exceptions import ObjectDoesNotExist


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
    image_url = models.TextField(blank=True, default='../../static/img/default_apartment.png')

    def __str__(self):
        return f"Owner:{self.owner}, Address:{self.address}, City:{self.city}"

    @classmethod
    def get_apartment_by_id(cls, id):
        try:
            return cls.objects.get(owner__id=id)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def get_all_relevant_apartments(cls):
        return cls.objects.filter(is_relevant=True)
