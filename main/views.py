from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apartments.views import owner_home
from seekers.views import seeker_home


def index(request):
    if request.user.is_authenticated:
        return home(request)
    else:
        return render(request, 'main/landing_page.html')


@login_required
def home(request):
    if request.user.is_seeker:
        return seeker_home(request)
    elif request.user.is_owner:
        return owner_home(request)
    else:
        return render(request, 'main/landing_page.html')


def register(request):
    return render(request, 'main/navigation-page-register.html')
