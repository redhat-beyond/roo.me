from django.shortcuts import render


def search(request):
    return render(request, 'search/search.html')
