from django.contrib import admin
from .models import User, Hobby
from seekers.models import Seeker
from apartments.models import Apartment, City
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdminConfig(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'is_active',)

    fieldsets = (
        ('Overview', {'fields': ('email', 'first_name', 'last_name',
                                 'birth_date', 'date_joined',
                                 'is_active', 'hobbies', 'image_url')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
        ('properties', {'fields': ('not_smoking', 'pets_allowed',
                                   'air_conditioner', 'balcony',
                                   'elevator', 'long_term',
                                   'immediate_entry',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'birth_date',
                       'is_staff', 'is_active',
                       'is_superuser', 'hobbies', 'image_url',
                       'not_smoking', 'pets_allowed',
                       'air_conditioner', 'balcony',
                       'elevator', 'long_term',
                       'immediate_entry',),
        }),
    )


@admin.register(Apartment)
class ApartmentAdminConfig(admin.ModelAdmin):
    list_display = ('owner', 'date_posted', 'city', 'address', 'rent',
                    'num_of_roomates', 'num_of_rooms', 'start_date',)


@admin.register(City)
class CityAdminConfig(admin.ModelAdmin):
    pass


@admin.register(Hobby)
class HobbyAdminConfig(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Seeker)
class SeekerAdminConfig(admin.ModelAdmin):
    list_display = ('base_user', 'city', 'start_date', 'min_rent', 'max_rent',
                    'num_of_roomates', 'num_of_rooms', 'about')
