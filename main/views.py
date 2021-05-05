from django.shortcuts import render


def home(request):
    if request.user.is_authenticated:
        return render(request, 'main/home.html')
    return render(request, 'main/landing_page.html')


def register(request):
    return render(request, 'main/navigation-page-register.html')
