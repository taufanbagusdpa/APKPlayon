from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from django.db.models import F
from apps.models import SubCategory
from books.models import *
from bs4 import BeautifulSoup
from django.conf import settings
import datetime
import base64
import urllib.request

def scraping(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    soup = BeautifulSoup(source, 'lxml')
    image = soup.find_all('img', class_='T75of QNCnCf')
    title = soup.find_all('div', class_='WsMG1c nnK0zc')
    subtitle = soup.find_all('a', class_='mnKHRc')
    price = soup.find_all('span', class_='VfPpfd ZdBevf i5DZme')
    star = soup.find_all('div', {"role":"img"})
    href = soup.find_all('div', class_='b8cIId ReQCgd Q9MA7b')

    titles = []
    stars = []
    subtitles = []
    prices = []
    hrefs = []
    srcs = []

    srcs_value = []
    subtitles_value = []
    array = []

    def fun(title, image, url, price, star, writer):
        dicts = dict();
        dicts['title']   = title
        dicts['image']   = image
        dicts['url']     = url
        dicts['price']  = price
        dicts['star']   = star
        dicts['writer']   = writer
        array.append(dicts)

    minarr = min(len(image),len(title),len(subtitle),len(price),len(star),len(href))

    for index in range(0,len(image),3):
        srcs_value.append(image[index].get("data-src").replace('https://', ''))

    for index in range(len(subtitle)):
        if subtitle[index].text == None:
            continue
        else:
            subtitles_value.append(subtitle[index].text)

    for index,i in enumerate(range(minarr)):
        if "/audiobooks/" in (href[index].find("a", class_="")).get('href'):
            continue
        else:
            fun(
                title[index].text,
                srcs_value[index].replace(' ',''),
                ((href[index].find("a", class_="")).get('href')).replace('/store',''),
                price[index].text,
                (star[index].get("aria-label").replace(' stars out of five stars','')).replace('Rated ',''),
                subtitles_value[index]
            )

    return array

def index(request, template="books.html"):
    url = 'https://play.google.com/store/books?hl=en'
    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Books on "+settings.APP_NAME,
        "name": "books",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=3),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_books.html",
        "current_url": request.build_absolute_uri
    }
    return render_to_response(template, data)

def top(request, template="books.html"):
    url = 'https://play.google.com/store/books/top?hl=en'
    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Top Charts - Books on "+settings.APP_NAME,
        "name": "books",
        "subname": "top",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=3),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_books.html",
        "current_url": request.build_absolute_uri
    }
    return render_to_response(template, data)

def new(request, template="books.html"):
    url = 'https://play.google.com/store/books/new?hl=en'
    data = {
        "appName": settings.APP_NAME,
        "appTitle": "New Releases - Books on "+settings.APP_NAME,
        "name": "books",
        "subname": "new",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=3),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_books.html",
        "current_url": request.build_absolute_uri
    }
    return render_to_response(template, data)

def category(request, slug):
    url = "https://play.google.com/store/books/category/"+slug+"?hl=en"

    name = SubCategory.objects.values_list('name', flat=True).filter(link=slug,id_subcategory=3)

    data = {
        "appName": settings.APP_NAME,
        "appTitle": name[0]+" - Books on "+settings.APP_NAME,
        "name": "books",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=3),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_books.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response("books.html", data)

def details_posts(request, slug_posts):
    id_posts = request.GET.get('id')
    source = requests.get('https://play.google.com/store/books/details/'+slug_posts+'?id='+id_posts+'&hl=en').text
    soup = BeautifulSoup(source, 'lxml')
    img = soup.find('img', attrs={'itemprop':'image'})
    title = soup.find_all('h1', class_="AHFaub")
    writer = soup.find('span', class_='UAO9ie')
    star = soup.find('div',attrs={'role':'img'})
    review = soup.find_all('span', class_="AYi5wd ddprqc")
    desc = soup.find("div", attrs={'itemprop':'description'})
    add = soup.find_all('span', class_='htlgb')
    publisher = soup.find_all('div', class_='uN7Lic')

    def functitle():
        for index, i in enumerate(title):
            return i.find("span", class_='').text

    def funcpub():
        for index, i in enumerate(publisher):
            return (i.find("span", class_='').text).replace("Sold by ","")

    def funcreview():
        for index, i in enumerate(review):
            return i.find("span", class_='').text

    def funcadditional():
        arrayactor = []
        for i in add:
            arrayactor.append(i.text)
        return arrayactor

    exist = posts.objects.filter(id=id_posts)
    if exist.exists() == True:
        exist.update(view=F('view')+1,updated_at=datetime.datetime.now())
    else:
        inserts_posts = posts(id=id_posts,
                        slug = slug_posts,
                        link = "https://play.google.com/store/books/details/"+slug_posts+"?id="+id_posts,
                        image = img.get("src"),
                        title = functitle(),
                        content = desc.text,
                        view = '0',
                        updated_at = datetime.datetime.now(),
                        created_at = datetime.datetime.now()
                        )
        inserts_posts.save()

        inserts_details = details(id_posts_id = id_posts,
                        star = star.get('aria-label').replace('Rated ',"").replace(' stars out of five stars',""),
                        rating = funcreview(),
                        author = writer.text,
                        publisher = funcpub()
                        )
        inserts_details.save()

        insert_additional = additional(id_posts_id = id_posts, name="-".join(funcadditional()))
        insert_additional.save()

    return redirect('/books/'+id_posts+'/'+slug_posts)

def booksposts(request, id, slug):
    post = posts.objects.all().filter(id=id)
    books_details = details.objects.filter(id_posts_id=post[0].id)
    books_additional = additional.objects.filter(id_posts_id=post[0].id)

    data = {
        "appName": settings.APP_NAME,
        "appTitle": post[0].title+" - Books on "+settings.APP_NAME,
        "name": "books",
        "post": post,
        "details": books_details,
        "additional": books_additional[0].name.split('-'),
        "subcategory": SubCategory.objects.all().filter(id_subcategory=3),
        "sidebar": "./sidebars/sidebar_books.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response("posts/post_books.html",data)

def download(request, server, id):
    post = posts.objects.all().filter(id=id)
    encodedBytes = base64.b64encode((post[0].link).encode("utf-8"))
    encodedStr = str(encodedBytes, "utf-8")
    link = post[0].link

    if server == 'server1':
        config = settings.SERVER1
        if config == 'adf.ly':
            uri = "http://api.adf.ly/api.php?key="+settings.ADFLYAPI+"&uid="+settings.ADFLYUID+"&advert_type=int&domain=adf.ly&url="+link+""
            return HttpResponseRedirect(urllib.request.urlopen(uri).read(1000))
        elif config == 'sh.st':
            redirect = "http://sh.st/st/"+settings.SHSTAPI+"/"+link+""
            return HttpResponseRedirect(redirect)
        elif config == 'bit.ly':
            uri = "https://api-ssl.bitly.com/v3/shorten?access_token="+settings.BITLYAPI+"&longUrl="+link+""
            return HttpResponseRedirect((json.loads((requests.get(uri)).content))['data']['url'])

    if server == 'server2':
        config = settings.SERVER2
        if config == 'adf.ly':
            uri = "http://api.adf.ly/api.php?key="+settings.ADFLYAPI+"&uid="+settings.ADFLYUID+"&advert_type=int&domain=adf.ly&url="+link+""
            return HttpResponseRedirect(urllib.request.urlopen(uri).read(1000))
        elif config == 'sh.st':
            redirect = "http://sh.st/st/"+settings.SHSTAPI+"/"+link+""
            return HttpResponseRedirect(redirect)
        elif config == 'bit.ly':
            uri = "https://api-ssl.bitly.com/v3/shorten?access_token="+settings.BITLYAPI+"&longUrl="+link+""
            return HttpResponseRedirect((json.loads((requests.get(uri)).content))['data']['url'])
