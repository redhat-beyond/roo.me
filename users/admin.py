from django.contrib import admin
from .models import User, Apartment, City, Hobby
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdminConfig(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'is_active',)

    fieldsets = (
        ('Overview', {'fields': ('email', 'first_name', 'last_name',
                                 'birth_date', 'date_joined',
                                 'is_active', 'hobbies')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'birth_date',
                       'is_staff', 'is_active',
                       'is_superuser', 'hobbies'),
        }),
    )


@admin.register(Apartment)
class ApartmentAdminConfig(admin.ModelAdmin):
    list_display = ('owner', 'datePosted', 'city', 'address', 'rentPricePerMonth',
                    'numOfRoomates', 'numOfRooms', 'startDate')


@admin.register(City)
class CityAdminConfig(admin.ModelAdmin):
    pass


@admin.register(Hobby)
class HobbyAdminConfig(admin.ModelAdmin):
    list_display = ('name',)
