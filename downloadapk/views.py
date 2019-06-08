from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
import requests
import json
from django.http import HttpResponse
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.defaultfilters import slugify
from .forms import SearchForm
from django.template import RequestContext
from apps.models import *
from django.db.models import F
from movies import views as moviesviews
from books import views as booksviews
from django.urls import resolve

def scraping(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    image = soup.find_all('img', class_='cover-image')
    title = soup.find_all('a', class_='title')
    star = soup.find_all('div', class_='tiny-star')
    subtitle = soup.find_all('a', class_='subtitle')

    a = []
    b = []
    c = []
    d = []
    e = []

    array = []

    def fun(title, href, image, subtitle,star):
        dicts = dict();
        dicts['title']   = title
        dicts['url']    = href.replace('?id=','/'+slugify(title).replace("-","_")+'?id=')
        dicts['image']   = image
        dicts['subtitle']   = subtitle
        dicts['star']   = star
        array.append(dicts)

    for index in range(len(image)):
        a.append(title[index].get("title"))
        b.append(title[index].get("href").replace('/store',''))
        c.append(image[index].get("src").replace('https://', ''))

    for index in range(len(subtitle)):
        if subtitle[index].get("title") == None:
            continue
        else:
            d.append(subtitle[index].get("title"))

    for index, i in enumerate(star):
        e.append(star[index].get("aria-label").replace(' stars out of five stars ',''))

    for index in range(len(e)):
        fun(a[index],b[index],c[index].replace('//', ''),d[index],e[index].replace(' Rated ', ''))

    return array

def index(request, template="index.html"):
    url = 'https://play.google.com/store/apps/top?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": settings.APP_NAME,
        "name": "entertaiment",
        "array": scraping(url),
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def post(request):
    context = RequestContext(request)
    q = slugify(request.POST.get("q")).replace("-","+")
    c = "apps"
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            exist = keywords.objects.filter(slug=q)
            if exist.exists() == True:
                exist.update(view=F('view')+1,updated_at=datetime.datetime.now())
            else:
                inserts_keywords = keywords(
                                query = request.POST.get("q"),
                                slug = q,
                                view = '0',
                                updated_at = datetime.datetime.now(),
                                created_at = datetime.datetime.now()
                                )
                inserts_keywords.save()
            return redirect('/store/search?q='+q+'&c='+c)
        else:
            return HttpResponse(form.errors)
    else:
        form = SearchForm()

def search(request, search):

    scraping_apps = None
    appTitle = None
    viewsearch = None

    if request.GET.get("c") == "apps":
        appTitle = request.GET.get("q").title()+" - Android Apps on "+settings.APP_NAME
        scraping_apps = scraping("https://play.google.com/store/search?q="+slugify(request.GET.get("q")).replace("-","+")+"&c="+request.GET.get("c")+"&hl=en")
        viewsearch = "searchs/search_apps.html"
    elif request.GET.get("c") == "movies":
        appTitle = request.GET.get("q").title()+" - Movies on "+settings.APP_NAME
        scraping_apps = moviesviews.scraping("https://play.google.com/store/search?q="+slugify(request.GET.get("q")).replace("-","+")+"&c="+request.GET.get("c")+"&hl=en")
        viewsearch = "searchs/search_movies.html"
    else:
        appTitle = request.GET.get("q").title()+" - Books on "+settings.APP_NAME
        scraping_apps = booksviews.scraping("https://play.google.com/store/search?q="+slugify(request.GET.get("q")).replace("-","+")+"&c="+request.GET.get("c")+"&hl=en")
        viewsearch = "searchs/search_books.html"

    data = {
        "appName": settings.APP_NAME,
        "appTitle": appTitle,
        "name": "search",
        "q": request.GET.get("q"),
        "c": request.GET.get("c"),
        "array": scraping_apps,
        "current_url": request.build_absolute_uri
    }
    return render_to_response(viewsearch, data)

def pages(request):
    current_url = resolve(request.path_info).url_name
    viewsearch = "pages/"+current_url+".html"
    data = {
        "appName": settings.APP_NAME,
        "appTitle": slugify(current_url).replace("-"," ").title()+' - '+settings.APP_NAME,
        "title": slugify(current_url).replace("-"," ").title(),
        "current_url": request.build_absolute_uri
    }
    return render_to_response(viewsearch, data)
