from django.shortcuts import render
from .models import Desease
from django.db.models import Q
from googletrans import Translator
import speech_recognition as sr

useless_words = [
        "About","Above","According to","Across","After","Against","Ahead of","Along","Amidst","Among","Amongst","Apart from",
        "Around","As","As far as","As well as","Aside from","At","Barring","Because of","Before","Behind","Below","Beneath","Beside","Besides","Between",
        "Beyond","By","By means of","Circa","Concerning","Despite","Down","Due to","During","In","In accordance with","In addition to","In case of",
        "In front of","In lieu of","In place of","In spite of","In to","Inside","Instead of","Into","Except","Except for","Excluding","For","Following",
        "From","Like","Minus","Near","Next","Next to","Past","Per","Prior to","Round","Since","Off","On","On account of","On behalf of","On to",
        "On top of","Onto","Opposite","Out","Out from","Out of","Outside","Over","Owing to","Plus","Than","Through","Throughout","Till","Times",
        "To","Toward","Towards","Under","Underneath","Unlike","Until","Unto","Up","Upon","Via","With","With a view to","Within","Without","a","an","the",
    ]

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
    initital_query = query
    query1 = Translator(service_urls=['translate.googleapis.com']).translate(text=query, dest='en')
    
    this_language = query1.src
    query = query1.text
    
    query = query.split()
    res = []
    
    for i in query:
        if(i not in useless_words):
            res+=list(Desease.objects.filter
            (
                Q(Disease_name__icontains=i) | 
                Q(Disease_description__icontains=i) |
                Q(Disease_symptoms__icontains=i) |
                Q(Disease_remidies__icontains=i) 
            ))
    res = list(set(res))

    if(this_language != 'en'):
        for i in res:
            i.Disease_name = Translator(service_urls=['translate.googleapis.com']).translate(text=i.Disease_name, dest=this_language).text
    return render(request, "main/search.html", {"found_desease":res, "query":initital_query, "useless_words":useless_words})

def voice_search(request):
    r2 = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r2.listen(source)
        try:
            get = r2.recognize_google(audio)
            s1 = Translator(service_urls=['translate.googleapis.com']).translate(text=get, dest='en')
            
            this_language = s1.src
            s = s1.text
            s = s.split()
            res = []
            
            for i in s:
                if(i not in useless_words):
                    res+=list(Desease.objects.filter(
                        Q(Disease_name__icontains=i) | 
                        Q(Disease_description__icontains=i) |
                        Q(Disease_symptoms__icontains=i) |
                        Q(Disease_remidies__icontains=i) 
                    ))

            res = list(set(res))
            if(this_language != 'en'):
                for i in res:
                    i.Disease_name = Translator(service_urls=['translate.googleapis.com']).translate(text=i.Disease_name, dest=this_language).text

            return render(request, "main/search.html", {"found_desease":res, "query":get})
        except:
            pass

def about(request):
    return render(request, "main/about.html")