from django.urls import path
from . import views as user_views


urlpatterns = [
    path('update/', user_views.update_user, name='update-user'),
    path('password_change/', user_views.password_change, name='change-password'),
    path('<int:user_id>/details', user_views.user_details, name='user-details'),
]
