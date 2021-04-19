from django.contrib import admin
from .models import Connection


@admin.register(Connection)
class ConnectionAdminConfig(admin.ModelAdmin):
    list_display = ('apartment', 'seeker', 'date_created')
