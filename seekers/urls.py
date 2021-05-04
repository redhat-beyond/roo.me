from django.urls import path
from . import views as seeker_views


urlpatterns = [
    path('register/', seeker_views.register_seeker, name='register_seeker'),
]
