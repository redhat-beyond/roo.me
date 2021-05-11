from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Connection, ConnectionType


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
