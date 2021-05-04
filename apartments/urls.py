from django.urls import path
from . import views as apartment_views

urlpatterns = [
    path('update', apartment_views.updateApartment, name='apartment-update'),
    path('register/', apartment_views.register_apartment, name='register_apartment'),
]
