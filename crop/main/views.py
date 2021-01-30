from django.shortcuts import render
from .models import Desease
from django.db.models import Q
from googletrans import Translator
import speech_recognition as sr
from selenium import webdriver
from bs4 import BeautifulSoup
import cloudscraper
import html5lib


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
    
    search_scrapper_res, ob = search_scrapper(query)
    request.session['passing'] = ob

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
        for i in search_scrapper_res:
            i[0] = Translator(service_urls=['translate.googleapis.com']).translate(text=i[0], dest=this_language).text
    return render(request, "main/search.html", {"found_desease":res, "query":initital_query, "useless_words":useless_words, "found_scrap": search_scrapper_res})

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

def desease_scrap(request, pk):
    store = request.session['passing']
    out = urlOpener_scrapper(store[int(pk)])
    return render(request, "main/scrap_out.html", {"out": out})

def search_scrapper(inp):
    store = []
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=options)
    
    
    inp = "%20".join(inp.split())
    url = "https://www.gardeningknowhow.com/search?q="+inp
    print(url)
    driver.get(url) #navigate to the page
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    out = soup.find_all('a', {'class', 'gs-title'})
    search_res = []
    old_i = ''
    count=-1
    for i in out:
        count += 1
        store.append(str(i).split()[2][13:-1])
        if(old_i == i):
            continue
        old_i = i
        b = i.get_text()
        if(b == ' '):
            break

        
        search_res.append([b, str(count)])
    return(search_res, store)

def urlOpener_scrapper(url):
    scraper = cloudscraper.create_scraper()
    htmlContent = scraper.get(url).content
    soup = BeautifulSoup(htmlContent, 'html.parser')
    paragraph = soup.find('div', id="main-art")
    tot = []
    head = []
    para = []
    for i in paragraph.contents:
        if(str(i)[1:3] == "h2"):
            tot.append([head, para])
            head = []
            para = []
            head.append(i)
        else:
            para.append(i)
    tot.append([head,para])
    
    output = {}
    for i in tot[1:]:
        heading = i[0][0].get_text()
        sub_out = []
        for j in i[1]:
            soup = BeautifulSoup(str(j), "html.parser")
            sub_out.append(soup.get_text().strip())

        output[heading] = sub_out
    return output
    