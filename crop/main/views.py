from django.shortcuts import render
from .models import Desease
from django.db.models import Q

def homepage(request):
    return render(
        request, 
        "main/home.html", 
        {"desease":Desease.objects.all}
    )

def desease(request, pk):
    d = Desease.objects.get(id = pk)

    return render(
        request,
        "main/desease.html",
        {"desease": d}
    )

def search(request):
    query = request.GET['quary']
    res = Desease.objects.filter(
        Q(desease_name__icontains=query) | 
        Q(desease_description__icontains=query)
    )
    return render(request, "main/search.html", {"found_desease":list(set(res))})
