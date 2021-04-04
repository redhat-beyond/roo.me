from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ('date_joined',)
    list_display = ('email', 'first_name', 'last_name',
                    'is_staff', 'is_superuser', 'is_active',)

    fieldsets = (
        ('Overview', {'fields': ('email', 'first_name', 'last_name',
                                 'birth_date', 'date_joined',
                                 'is_active',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                       'first_name', 'last_name', 'birth_date',
                       'is_staff', 'is_active',
                       'is_superuser',),
        }),
    )


admin.site.register(User, UserAdminConfig)
