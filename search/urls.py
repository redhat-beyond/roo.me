from django.urls import path
from . import views as search_views


urlpatterns = [
    path('', search_views.search, name='search'),
]
