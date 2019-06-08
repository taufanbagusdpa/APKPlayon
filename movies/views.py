from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
import json
from django.db.models import F
from apps.models import SubCategory
from movies.models import *
from bs4 import BeautifulSoup
from django.conf import settings
import datetime


def scraping(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    image = soup.find_all('img', class_='cover-image')
    price = soup.find_all('span', class_='display-price')
    star = soup.find_all('div', class_='tiny-star')
    genre = soup.find_all('a', class_='subtitle subtitle-movie-category')
    href = soup.find_all('a', class_='title', attrs={'aria-hidden':'true'})

    stars = []
    genres = []
    prices = []
    hrefs = []
    alts = []
    srcs = []

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

    for index, i in enumerate(genre):
        genres.append(genre[index].text)

    for index, i in enumerate(price):
        if index%2==0:
            prices.append(price[index].text)
        else:
            continue

    for i in range(0, len(href)):
        if "/store/tv/show" in href[i].get("href"):
            continue
        else:
            hrefs.append(href[i].get("href").replace('/store',''))
            alts.append(image[i].get("alt"))
            srcs.append(image[i].get("src").replace('https://', ''))

    minarr = min(len(stars),len(prices),len(hrefs),len(alts),len(srcs))

    try:
        for index in range(minarr):
            fun(alts[index],srcs[index],hrefs[index],prices[index],int(float(stars[index].replace(' Rated ', ''))))
    except IndexError:
        array = None

    return array

def index(request, template="movies.html"):
    url = 'https://play.google.com/store/movies?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Movies on "+settings.APP_NAME,
        "name": "movies",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=2),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_movies.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def top(request, template="movies.html"):
    url = 'https://play.google.com/store/movies/top?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Top Movies - Movies on "+settings.APP_NAME,
        "name": "movies",
        "subname": "top",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=2),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_movies.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def new(request, template="movies.html"):
    url = 'https://play.google.com/store/movies/new?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "New Movies Releases - Movies on "+settings.APP_NAME,
        "name": "movies",
        "subname": "new",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=2),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_movies.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def category(request, slug):
    url = "https://play.google.com/store/movies/category/"+slug+"?hl=en"

    name = SubCategory.objects.values_list('name', flat=True).filter(link=slug, id_subcategory=2)

    data = {
        "appName": settings.APP_NAME,
        "appTitle": name[0]+" - Movies on "+settings.APP_NAME,
        "name": "movies",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=2),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_movies.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response("movies.html", data)

def details_posts(request, slug_posts):
    id_posts = request.GET.get('id')
    source = requests.get('https://play.google.com/store/movies/details/'+slug_posts+'?id='+id_posts+'&hl=en').text
    soup = BeautifulSoup(source, 'lxml')
    img = soup.find('img', attrs={'itemprop':'image'})
    title = soup.find_all('span', class_="")
    release = soup.find('span', class_='UAO9ie')
    duration = soup.find('meta',attrs={'itemprop':'duration'})
    star = soup.find('div',attrs={'role':'img'})
    rating = soup.find_all('span', class_="")
    genre = soup.find('a',attrs={'itemprop':'genre'})
    video = soup.find('button', class_='lgooh ')
    desc = soup.find('meta',attrs={'name':'description'})
    dataactor = soup.find_all('span', attrs={'itemprop':'actor'})
    dataproducer = soup.find_all('span', attrs={'itemprop':'producer'})
    datadirector = soup.find_all('span', attrs={'itemprop':'director'})
    datawriter = soup.find_all('span', attrs={'itemprop':'writer'})
    dataadditional = soup.find_all('span', class_='htlgb')

    def funvideo():
        if video == None:
            return None
        else:
            return video.get("data-trailer-url")

    def funduration():
        if duration == None:
            return "Unknown"
        else:
            return duration.get('content').replace('M0S',' Minutes')

    def funcactor():
        arrayactor = []
        for i in dataactor:
            arrayactor.append(i.text.replace(', ',''))
        return arrayactor

    def funcproducer():
        producer = []
        for i in dataproducer:
            producer.append(i.text.replace(', ',''))
        return producer

    def funcdirector():
        arrayactor = []
        for i in datadirector:
            arrayactor.append(i.text.replace(', ',''))
        return arrayactor

    def funcwriter():
        arrayactor = []
        for i in datawriter:
            arrayactor.append(i.text.replace(', ',''))
        return arrayactor

    def funcadditional():
        last_value = None
        arrayactor = []
        for i in dataadditional:
            if i.text == last_value:
                continue
            elif i.text == 'Available':
                continue
            elif i.text == 'Enabled':
                continue
            else:
                arrayactor.append(i.text)
                last_value = i.text
        return arrayactor

    exist = posts.objects.filter(id=id_posts)
    if exist.exists() == True:
        exist.update(view=F('view')+1,updated_at=datetime.datetime.now())
    else:
        inserts_posts = posts(id=id_posts,
                        slug = slug_posts,
                        link = "https://play.google.com/store/movies/details/"+slug_posts+"?id="+id_posts,
                        image = img.get("src"),
                        title = title[1].text,
                        content = desc.get('content'),
                        view = '0',
                        updated_at = datetime.datetime.now(),
                        created_at = datetime.datetime.now()
                        )
        inserts_posts.save()

        inserts_details = details(id_posts_id = id_posts,
                        star = star.get('aria-label').replace('Rated ',"").replace(' stars out of five stars',""),
                        genre = genre.text,
                        rating = rating[3].text,
                        release = release.text,
                        duration = funduration(),
                        video = funvideo(),
                        )
        inserts_details.save()

        insert_actor = actor(id_posts_id = id_posts, name=",".join(funcactor()))
        insert_actor.save()

        insert_producer = producer(id_posts_id = id_posts, name=",".join(funcproducer()))
        insert_producer.save()

        insert_director = director(id_posts_id = id_posts, name=",".join(funcdirector()))
        insert_director.save()

        insert_writer = writer(id_posts_id = id_posts, name=",".join(funcwriter()))
        insert_writer.save()

        insert_additional = additional(id_posts_id = id_posts, name=",".join(funcadditional()))
        insert_additional.save()

    return redirect('/movies/'+id_posts+'/'+slug_posts)

def moviesposts(request, id, slug):
    post = posts.objects.all().filter(id=id)
    movies_details = details.objects.filter(id_posts_id=post[0].id)
    movies_actor = actor.objects.filter(id_posts_id=post[0].id)
    movies_producer = producer.objects.filter(id_posts_id=post[0].id)
    movies_director = director.objects.filter(id_posts_id=post[0].id)
    movies_writer = writer.objects.filter(id_posts_id=post[0].id)
    movies_additional = additional.objects.filter(id_posts_id=post[0].id)

    slug = SubCategory.objects.filter(name=movies_details[0].genre)

    # url = "https://play.google.com/store/movies/category/"+slug[0].link+"?hl=en"

    data = {
        "appName": settings.APP_NAME,
        "appTitle": post[0].title+" Full Movie ("+movies_details[0].release+")",
        "name": "movies",
        "post": post,
        "details": movies_details,
        "actor": movies_actor[0].name.split(','),
        "producer": movies_producer[0].name.split(','),
        "director": movies_director[0].name.split(','),
        "writer": movies_writer[0].name.split(','),
        "additional": movies_additional[0].name.split(','),
        "subcategory": SubCategory.objects.all().filter(id_subcategory=2),
        "sidebar": "./sidebars/sidebar_movies.html",
        "current_url": request.build_absolute_uri,
        # "array": scraping(url)
    }

    return render_to_response("posts/post_movies.html",data)
