from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
import json
from django.db.models import F
from apps.models import SubCategory
from books.models import *
from bs4 import BeautifulSoup
from django.conf import settings
import datetime

def scraping(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    image = soup.find_all('img', class_='cover-image')
    price = soup.find_all('span', class_='display-price')
    star = soup.find_all('div', class_='tiny-star')
    href = soup.find_all('a', class_='card-click-target', attrs={'data-uitype':'500'})

    alts = []
    srcs = []
    prices = []
    hrefs = []
    stars = []

    array = []

    def fun(title, image, url, price, star):
        dicts = dict();
        dicts['title']   = title
        dicts['image']   = image
        dicts['url']     = url
        dicts['price']  = price
        dicts['star']   = star
        array.append(dicts)

    for index, i in enumerate(star):
        stars.append(star[index].get("aria-label").replace(' stars out of five stars ',''))

    for index, i in enumerate(price):
        if index%2==0:
            prices.append(price[index].text)
        else:
            continue

    for i in range(0, len(href)):
        if "/audiobooks/" in href[i].get("href"):
            continue
        else:
            hrefs.append(href[i].get("href").replace('/store',''))
            alts.append(image[i].get("alt"))
            srcs.append(image[i].get("src").replace('https://', ''))

    minarr = min(len(alts),len(srcs),len(hrefs),len(prices),len(stars))

    try:
        for index in range(minarr):
            fun(alts[index],srcs[index],hrefs[index],prices[index],int(float(stars[index].replace(' Rated ', ''))))
    except IndexError:
        array = None

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
    title = soup.find_all('span', class_="")
    writer = soup.find('span', class_='UAO9ie')
    star = soup.find('div',attrs={'role':'img'})
    rating = soup.find_all('span', class_="")
    desc = soup.find('content')
    add = soup.find_all('span', class_='htlgb')

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
                        title = title[1].text,
                        content = desc.text,
                        view = '0',
                        updated_at = datetime.datetime.now(),
                        created_at = datetime.datetime.now()
                        )
        inserts_posts.save()

        inserts_details = details(id_posts_id = id_posts,
                        star = star.get('aria-label').replace('Rated ',"").replace(' stars out of five stars',""),
                        rating = rating[3].text,
                        author = writer.text,
                        publisher = title[2].text
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
