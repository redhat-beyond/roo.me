from django.urls import path
from . import views as seeker_views


urlpatterns = [
    path('', seeker_views.search, name='search'),
]
