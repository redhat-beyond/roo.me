from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from .models import User
from .forms import UserUpdateForm


@login_required
def update_user(request):
    if request.method == 'POST':
        update_settings_form = UserUpdateForm(request.POST, instance=request.user)
        if update_settings_form.is_valid():
            update_settings_form.save(commit=True)
            return redirect('update-user')
    else:
        update_settings_form = UserUpdateForm(instance=request.user)
    return render(request, 'users/update.html', {
        'settings_form': update_settings_form
    })


@login_required
def password_change(request):
    if request.method == 'POST':
        password_change_form = auth_views.PasswordChangeForm(user=request.user, data=request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, password_change_form.user)
            return redirect('update-user')
    else:
        password_change_form = auth_views.PasswordChangeForm(user=request.user)
    return render(request, 'users/change-password.html', {
        'form': password_change_form
    })


def user_details(request, user_id):
    user_to_view = User.objects.filter(id=user_id).first()
    if not user_to_view:
        return redirect('home')
    else:
        hobbies_of_user = user_to_view.hobbies.all()
        return render(request, 'users/user-details.html', {
            'user': user_to_view,
            'hobbies': hobbies_of_user,
            })
