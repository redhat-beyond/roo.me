from django.contrib import admin
from .models import Connection, Message


@admin.register(Connection)
class ConnectionAdminConfig(admin.ModelAdmin):
    list_display = ('apartment', 'seeker', 'date_created', 'status')


@admin.register(Message)
class MessageAdminConfig(admin.ModelAdmin):
    list_display = ('connection', 'author', 'date_written')
