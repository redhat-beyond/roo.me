from django.shortcuts import render, redirect
from users.forms import UserCreationForm
from .forms import SeekerCreationForm
from main.decorators import not_logged_in_required


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
            return redirect('login')
    else:
        user_creation_form = UserCreationForm()
        seeker_creation_form = SeekerCreationForm()
    return render(request, 'seekers/seeker_register.html', {
        "uform": user_creation_form,
        "sform": seeker_creation_form,
        })
