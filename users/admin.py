from django.contrib import admin
from .models import User, Hobby, Seeker
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
                       'is_superuser', 'hobbies',
                       'not_smoking', 'pets_allowed',
                       'air_conditioner', 'balcony',
                       'elevator', 'long_term',
                       'immediate_entry',),
        }),
    )


@admin.register(Hobby)
class HobbyAdminConfig(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Seeker)
class SeekerAdminConfig(admin.ModelAdmin):
    list_display = ('base_user', 'city', 'start_date', 'min_rent', 'max_rent',
                    'num_of_roomates', 'num_of_rooms', 'about')
