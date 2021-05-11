from django.shortcuts import render


def home(request):
    if not request.user.is_authenticated:
        return render(request, 'main/landing_page.html')
    elif request.user.is_seeker:
        ''' TODO: delete current render and create a render_seeker_home
            function that will render the homepage for the seeker.'''
        return render(request, 'main/home.html')
    elif request.user.is_owner:
        ''' TODO: delete current render and create a render_owner_home
            function that will render the homepage for the owner.'''
        return render(request, 'main/home.html')
    else:
        return render(request, 'main/landing_page.html')


def register(request):
    return render(request, 'main/navigation-page-register.html')
