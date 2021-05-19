from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from main.decorators import not_logged_in_required
from users.forms import UserCreationForm, QualitiesForm
from .forms import SeekerCreationForm, SeekerUpdateForm


@not_logged_in_required(redirect_to='home')
def register_seeker(request):
    if request.method == 'POST':
        user_creation_form = UserCreationForm(request.POST)
        seeker_creation_form = SeekerCreationForm(request.POST)

        if seeker_creation_form.is_valid() and user_creation_form.is_valid():
            new_base_user = user_creation_form.save(commit=True)
            seeker_profile = seeker_creation_form.save(commit=False)
            seeker_profile.base_user = new_base_user
            seeker_profile.save()
            messages.success(request, f"Seeker profile {new_base_user} created successfully! You can log in now.")
            return redirect('login')
    else:
        user_creation_form = UserCreationForm()
        seeker_creation_form = SeekerCreationForm()
    return render(request, 'seekers/seeker_register.html', {
        "uform": user_creation_form,
        "sform": seeker_creation_form,
        })


@login_required
def update_seeker(request):
    if not request.user.is_seeker:
        return redirect('home')

    if request.method == 'POST':
        seeker_form = SeekerUpdateForm(request.POST, instance=request.user.seeker)
        qualities_form = QualitiesForm(request.POST, instance=request.user)
        if seeker_form.is_valid() and qualities_form.is_valid():
            seeker_form.save()
            qualities_form.save()
            return redirect('seeker-update')
    else:
        seeker_form = SeekerUpdateForm(instance=request.user.seeker)
        qualities_form = QualitiesForm(instance=request.user)

    context = {
        'seeker_form': seeker_form,
        'qualities_form': qualities_form
    }

    return render(request, 'seekers/update-seeker.html', context)
