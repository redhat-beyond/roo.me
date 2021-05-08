from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.forms import UserCreationForm
from main.decorators import not_logged_in_required
from .forms import (ApartmentDetailsUpdateForm,
                    ApartmentQualitiesUpdateForm,
                    ApartmentCreationForm,)


@login_required
def updateApartment(request):
    if request.user.is_owner is False:
        return redirect('home')

    if request.method == 'POST':
        apartment_form = ApartmentDetailsUpdateForm(request.POST, instance=request.user.apartment)
        qualities_form = ApartmentQualitiesUpdateForm(request.POST, instance=request.user)
        if apartment_form.is_valid() and qualities_form.is_valid():
            apartment_form.save()
            qualities_form.save()
            return redirect('apartment-update')
    else:
        apartment_form = ApartmentDetailsUpdateForm(instance=request.user.apartment)
        qualities_form = ApartmentQualitiesUpdateForm(instance=request.user)

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
            return redirect('home')
    else:
        user_creation_form = UserCreationForm()
        apartment_creation_form = ApartmentCreationForm()
    return render(request, 'apartments/apartment_register.html', {
        "uform": user_creation_form,
        "aform": apartment_creation_form,
        })
