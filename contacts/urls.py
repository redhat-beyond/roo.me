from django.urls import path
from . import views as contacts_views

urlpatterns = [
    path('', contacts_views.contact_page, name='contact-page'),
    path('add/<int:apartment_id>', contacts_views.add_new_contact, name='add-contact'),
    path('decline/<int:apartment_id>', contacts_views.decline_apartment, name='decline-contact'),
    path('chat/<int:connection_id>', contacts_views.chat, name='chat'),
    path('<action>/<int:connection_id>', contacts_views.approve_or_reject_contact, name='approve-reject-contact'),
]
