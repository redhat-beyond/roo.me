from django.urls import path
from . import views

urlpatterns = [
    path('update', views.updateApartment, name='apartment-update'),
]
