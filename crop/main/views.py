from django.shortcuts import render
from .models import Desease
from django.db.models import Q
from googletrans import Translator

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
    query = Translator(service_urls=['translate.googleapis.com']).translate(text=query, dest='en').text
    res = Desease.objects.filter(
        Q(Disease_name__icontains=query) | 
        Q(Disease_description__icontains=query) |
        Q(Disease_symptoms__icontains=query) |
        Q(Disease_remidies__icontains=query) 
    )
    return render(request, "main/search.html", {"found_desease":list(set(res)), "query":query})
