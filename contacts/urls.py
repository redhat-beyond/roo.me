from django.urls import path
from . import views as contacts_views

urlpatterns = [
    path('', contacts_views.contact_page, name='contact-page'),
    path('add/<int:apartment_id>', contacts_views.add_new_contact, name='add-contact'),
]
