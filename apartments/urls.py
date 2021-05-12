from django.urls import path
from . import views as apartment_views

urlpatterns = [
    path('update', apartment_views.update_apartment, name='apartment-update'),
    path('register/', apartment_views.register_apartment, name='register_apartment'),
    path('<int:apartment_id>/details', apartment_views.apartment_details, name='apartment-details'),
]
