from django.shortcuts import render_to_response
from django.shortcuts import render
from django.shortcuts import redirect
import requests
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from django.db.models import F
from apps.models import SubCategory
from movies.models import *
from bs4 import BeautifulSoup
from django.conf import settings
import datetime
import base64
import urllib.request


def scraping(url):
    source = requests.get(url).text
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

    def fun(title, image, url, price, star,genre):
        dicts = dict();
        dicts['title']   = title
        dicts['image']   = image
        dicts['url']     = url
        dicts['price']  = price
        dicts['star']   = star
        dicts['genre']   = genre
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
        if "/store/tv/show" in (href[index].find("a", class_="")).get('href'):
            continue
        else:
            fun(
                title[index].text,
                srcs_value[index].replace(' ',''),
                ((href[index].find("a", class_="")).get('href')).replace('/store',''),
                price[index].text,
                (star[index].get("aria-label").replace(' stars out of five stars','')).replace('Rated ',''),
                subtitles_value[index-1]
            )

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
    title = soup.find_all('h1', class_="AHFaub")
    release = soup.find('span', class_='UAO9ie')
    duration = soup.find('meta',attrs={'itemprop':'duration'})
    star = soup.find('div',attrs={'role':'img'})
    review = soup.find_all('span', class_="AYi5wd sq4rZd")
    genre = soup.find('a',attrs={'itemprop':'genre'})
    video = soup.find('button', class_='lgooh ')
    desc = soup.find('meta',attrs={'name':'description'})
    dataactor = soup.find_all('span', attrs={'itemprop':'actor'})
    dataproducer = soup.find_all('span', attrs={'itemprop':'producer'})
    datadirector = soup.find_all('span', attrs={'itemprop':'director'})
    datawriter = soup.find_all('span', attrs={'itemprop':'writer'})
    dataadditional = soup.find_all('span', class_='htlgb')

    def functitle():
        for index, i in enumerate(title):
            return i.find("span", class_='').text

    def funcreview():
        for index, i in enumerate(review):
            return i.find("span", class_='').text

    def funcgenre():
        if genre == None:
            return "Unknown"
        else:
            return genre.text

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
                        title = functitle(),
                        content = desc.get('content'),
                        view = '0',
                        updated_at = datetime.datetime.now(),
                        created_at = datetime.datetime.now()
                        )
        inserts_posts.save()

        inserts_details = details(id_posts_id = id_posts,
                        star = star.get('aria-label').replace('Rated ',"").replace(' stars out of five stars',""),
                        genre = funcgenre(),
                        rating = funcreview(),
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
