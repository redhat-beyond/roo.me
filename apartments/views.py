from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.decorators import not_logged_in_required
from users.forms import UserCreationForm, QualitiesForm
from .forms import ApartmentDetailsUpdateForm, ApartmentCreationForm
from .models import Apartment
import main


@login_required
def update_apartment(request):
    if request.user.is_owner is False:
        return redirect('home')

    if request.method == 'POST':
        apartment_form = ApartmentDetailsUpdateForm(request.POST, instance=request.user.apartment)
        qualities_form = QualitiesForm(request.POST, instance=request.user)
        if apartment_form.is_valid() and qualities_form.is_valid():
            apartment_form.save()
            qualities_form.save()
            messages.success(request, "Apartment updated successfully!")
            return redirect('apartment-update')
    else:
        apartment_form = ApartmentDetailsUpdateForm(instance=request.user.apartment)
        qualities_form = QualitiesForm(instance=request.user)

    context = {
        'apartment_form': apartment_form,
        'qualities_form': qualities_form
    }

    return render(request, 'apartments/update-apartment.html', context)


@not_logged_in_required(redirect_to='home')
def register_apartment(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        apartment_creation_form = ApartmentCreationForm(request.POST)

        if apartment_creation_form.is_valid() and user_creation_form.is_valid():
            new_owner = user_creation_form.save(commit=True)
            apartment_profile = apartment_creation_form.save(commit=False)
            apartment_profile.owner = new_owner
            apartment_profile.save()
            messages.success(request, f"Owner profile {new_owner} created successfully! You can log in now.")
            return redirect('login')
    else:
        user_creation_form = UserCreationForm()
        apartment_creation_form = ApartmentCreationForm()
    return render(request, 'apartments/apartment_register.html', {
        "uform": user_creation_form,
        "aform": apartment_creation_form,
        })


@login_required()
def apartment_details(request, apartment_id):
    apartment_to_view = Apartment.get_apartment_by_id(apartment_id)

    if apartment_to_view is None:
        messages.warning(request, "Invalid apartment request!")
        return redirect(main.views.home)

    return render(request, 'apartments/apartment-details.html', {
         'apartment': apartment_to_view,
         })
