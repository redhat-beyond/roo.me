from django.urls import path
from . import views as seeker_views


urlpatterns = [
    path('update/', seeker_views.update_seeker, name='seeker-update'),
    path('register/', seeker_views.register_seeker, name='register_seeker'),
]
