from django.shortcuts import redirect


def not_logged_in_required(redirect_to='home'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_to)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
