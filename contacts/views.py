from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Connection, ConnectionType
from apartments.models import Apartment
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist


@login_required
def contact_page(request):
    pendings = Connection.get_connections_by_user(request.user, ConnectionType.PENDING)
    approved = Connection.get_connections_by_user(request.user, ConnectionType.APPROVED)
    is_owner = request.user.is_owner
    context = {
        'pending_connections': pendings,
        'approved_connections': approved,
    }
    if is_owner:
        return render(request, 'contacts/contact-page-owner.html', context)
    else:
        return render(request, 'contacts/contact-page-seeker.html', context)


@login_required
def add_new_contact(request, apartment_id):
    if not request.user.is_seeker:
        messages.warning(request, "You can't send a connection request!")
    else:
        try:
            apartment_to_add = Apartment.objects.get(pk=apartment_id)
        except ObjectDoesNotExist:
            apartment_to_add = None
        if apartment_to_add is None:
            messages.warning(request, "Invalid apartment request!")
        else:
            seeker_to_add = request.user.seeker
            new_connection = Connection(apartment=apartment_to_add, seeker=seeker_to_add)
            try:
                with transaction.atomic():
                    new_connection.save()
                    messages.success(request, "Connection request sent!")
            except IntegrityError:
                messages.warning(request, "You have already sent a connection request to this user!")

    return redirect('contact-page')


@login_required
def approve_or_reject_contact(request, action, connection_id):
    connection_to_action = Connection.get_connection_by_id(connection_id)
    if connection_to_action is None:
        messages.warning(request, "Invalid connection request!")
    else:
        connection_owner = connection_to_action.apartment.owner
        connection_seeker = connection_to_action.seeker.base_user
        if request.user != connection_owner:
            messages.warning(request, "You are not allowed to take action on this connection!")
        else:
            if action == 'approve':
                try:
                    connection_to_action.approve()
                    messages.success(request, f"You can now contact {connection_seeker.first_name}!")
                except ValueError:
                    messages.warning(request, "Can't approve this connection!")
            elif action == 'reject':
                connection_to_action.reject()
                messages.success(request, f"{connection_seeker.first_name} won't bother you anymore!")
            else:
                messages.warning(request, "Invalid connection action!")

    return redirect('contact-page')
