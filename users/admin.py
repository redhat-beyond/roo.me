from django.contrib import admin
from .models import User, Apartment, City
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdminConfig(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('email', 'first_name', 'last_name', 'user_type',
                    'is_staff', 'is_superuser', 'is_active',)

    fieldsets = (
        ('Overview', {'fields': ('email', 'first_name', 'last_name',
                                 'birth_date', 'date_joined', 'user_type',
                                 'is_active',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'birth_date', 'user_type',
                       'is_staff', 'is_active',
                       'is_superuser',),
        }),
    )


@admin.register(Apartment)
class ApartmentAdminConfig(admin.ModelAdmin):
    list_display = ('owner', 'datePosted', 'city', 'address', 'rentPricePerMonth',
                    'numOfRoomates', 'numOfRooms', 'startDate')


@admin.register(City)
class CityAdminConfig(admin.ModelAdmin):
    pass
