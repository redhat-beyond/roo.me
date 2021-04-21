from django.contrib import admin
from .models import Apartment, City


@admin.register(Apartment)
class ApartmentAdminConfig(admin.ModelAdmin):
    list_display = ('owner', 'date_posted', 'city', 'address', 'rent',
                    'num_of_roomates', 'num_of_rooms', 'start_date',)


@admin.register(City)
class CityAdminConfig(admin.ModelAdmin):
    pass
