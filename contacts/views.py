from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Connection, ConnectionType, Message
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
def decline_apartment(request, apartment_id):
    if not request.user.is_seeker:
        messages.warning(request, "You can't decline apartments!")
    else:
        try:
            apartment_to_decline = Apartment.objects.get(pk=apartment_id)
        except ObjectDoesNotExist:
            apartment_to_decline = None
        if apartment_to_decline is None:
            messages.warning(request, "Invalid apartment request!")
        else:
            seeker_to_add = request.user.seeker
            new_connection = Connection(apartment=apartment_to_decline, seeker=seeker_to_add)
            try:
                with transaction.atomic():
                    new_connection.save()
                    new_connection.reject()
                    messages.success(request, "This apartment will not pop up anymore")
            except IntegrityError:
                messages.warning(request, "You currently have a connection with this apartment!")

    return redirect('home')


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


@login_required
def chat(request, connection_id):
    chat_connection = Connection.get_connection_by_id(connection_id)
    if chat_connection is None:
        messages.warning(request, "Invalid request!")
    else:
        connection_owner = chat_connection.apartment.owner
        connection_seeker = chat_connection.seeker.base_user
        if ((request.user != connection_owner) and (request.user != connection_seeker)):
            messages.warning(request, "You are not allowed to enter this chat!")
        elif chat_connection.status != 'A':
            messages.warning(request, "This chat is yet to be approved!")
        else:
            if request.method == 'POST':
                msg = request.POST.get("msg_sent", "")
                if msg == "":
                    messages.warning(request, "Your message was empty!")
                else:
                    Message(connection=chat_connection, author=request.user, text=msg).save()
            chat_messages = chat_connection.get_chat_messages()
            if request.user.is_seeker:
                approved_contacts = Connection.objects.filter(
                    seeker__base_user=request.user,
                    status=ConnectionType.APPROVED,
                ).exclude(messages=None)
            else:
                approved_contacts = Connection.objects.filter(
                    apartment__owner=request.user,
                    status=ConnectionType.APPROVED,
                ).exclude(messages=None)
            recent_contacts = sorted(
                approved_contacts,
                key=lambda obj: obj.get_chat_messages().last().date_written,
                reverse=True
            )[:30]
            context = {
                'chat_messages': chat_messages,
                'recent_contacts': recent_contacts,
            }
            return render(request, 'contacts/chat.html', context)
    return redirect('contact-page')
