import hashlib
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import requests
import json
from bs4 import BeautifulSoup
from django.conf import settings
from apps.models import *
from apps.models import details as table_detail
import datetime
from django.db.models import F
global str
from django.db.models import Q

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

def index(request, template="apps.html"):
    url = 'https://play.google.com/store/apps/new?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Android Apps on "+settings.APP_NAME,
        "name": "apps",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=1),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_apps.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def top(request, template="apps.html"):
    url = 'https://play.google.com/store/apps/top?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "Top Charts - Android Apps on "+settings.APP_NAME,
        "name": "apps",
        "subname": "top",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=1),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_apps.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def new(request, template="apps.html"):
    url = 'https://play.google.com/store/apps/new?hl=en'

    data = {
        "appName": settings.APP_NAME,
        "appTitle": "New Releases - Android Apps on "+settings.APP_NAME,
        "name": "apps",
        "subname": "new",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=1),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_apps.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response(template, data)

def category(request, slug):
    if slug == "vr_top_device_featured_category":
        url = "https://play.google.com/store/apps/stream/"+slug+"?hl=en"
    elif slug == "FAMILY_AGE_RANGE1":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE1&hl=en"
    elif slug == "FAMILY_AGE_RANGE2":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE2&hl=en"
    elif slug == "FAMILY_AGE_RANGE3":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE3&hl=en"
    else:
        url = "https://play.google.com/store/apps/category/"+slug+"?hl=en"

    name = SubCategory.objects.values_list('name', flat=True).filter(link=slug,id_subcategory=1)

    data = {
        "appName": settings.APP_NAME,
        "appTitle": name[0]+" - Android Apps on "+settings.APP_NAME,
        "name": "apps",
        "subname": "home",
        "subcategory": SubCategory.objects.all().filter(id_subcategory=1),
        "array": scraping(url),
        "sidebar": "./sidebars/sidebar_apps.html",
        "current_url": request.build_absolute_uri
    }

    return render_to_response("apps.html", data)

def details_posts(request, slug_posts):
    id_posts = request.GET.get('id')
    source = requests.get('https://play.google.com/store/apps/details?id='+id_posts+'&hl=en').text
    soup = BeautifulSoup(source, 'lxml')
    info = soup.find_all('span', class_="htlgb")
    img = soup.find('img', attrs={'itemprop':'image'})
    title = soup.find_all('span', class_="")
    subtitle = soup.find_all('a', class_="hrTbp R8zArc")
    review = soup.find_all('span', class_="")
    content = soup.find('meta',attrs={'name':'description'})
    ss = soup.find_all('img', alt='Screenshot Image')
    dataadditional = soup.find_all('span', class_='htlgb')

    def funcadditional():
        last_value = None
        arrayadditional = []
        for i in dataadditional:
            if i.text == last_value:
                continue
            else:
                arrayadditional.append(i.text.replace(",","."))
                last_value = i.text
        return arrayadditional

    def funcss():
        arrayss = []
        for i in ss:
            if i.get("data-src") == None:
                continue
            elif i.get("data-src") == "data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==":
                continue
            elif i.get("data-src") == "data:image/gif;base64=w720-h310":
                continue
            elif i.get("data-src") == "":
                continue
            else:
                arrayss.append(i.get("data-src").replace("=w720-h310",""))
        return arrayss

    arradd = funcadditional()

    if id_posts == "com.mojang.minecraftpe":
        if arradd[4] == 'Varies with device':
            dataversion = slugify(arradd[4]).replace("-","_")
        else:
            dataversion = arradd[4]
    else:
        if arradd[3] == 'Varies with device':
            dataversion = slugify(arradd[3]).replace("-","_")
        else:
            dataversion = arradd[3]

    exist = posts.objects.filter(id=id_posts, version=dataversion)

    if exist.exists() == True:
        exist.update(view=F('view')+1,updated_at=datetime.datetime.now())
    else:
        inserts_posts = posts(id=id_posts,
                        slug = slugify(title[1].text).replace("-","_"),
                        link = "https://play.google.com/store/apps/details?id="+id_posts,
                        image = img.get("src"),
                        title = title[1].text,
                        content = content.get('content'),
                        version = dataversion,
                        view = '0',
                        updated_at = datetime.datetime.now(),
                        created_at = datetime.datetime.now()
                        )
        inserts_posts.save()

        inserts_ss = screenshot(id_posts_id=id_posts, image=",".join(funcss()))
        inserts_ss.save()

        inserts_details = table_detail(id_posts_id=id_posts,
                        developer = subtitle[0].text,
                        category = subtitle[1].text,
                        rating = review[2].text
                        )
        inserts_details.save()

        inserts_additional = additional(id_posts_id=id_posts, name=",".join(funcadditional()))
        inserts_additional.save()

    return redirect('/apps/'+dataversion+'/'+id_posts)


def appsposts(request, version, id):
    post = posts.objects.all().filter(id=id,version=version)
    apps_details = details.objects.filter(id_posts_id=post[0].id)
    apps_ss = screenshot.objects.filter(id_posts_id=post[0].id)
    apps_additional = additional.objects.filter(id_posts_id=post[0].id)

    slug = SubCategory.objects.filter(name=apps_details[0].category)

    if slug[0].link == "vr_top_device_featured_category":
        url = "https://play.google.com/store/apps/stream/"+slug[0].link+"?hl=en"
    elif slug[0].link == "FAMILY_AGE_RANGE1":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE1&hl=en"
    elif slug[0].link == "FAMILY_AGE_RANGE2":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE2&hl=en"
    elif slug[0].link == "FAMILY_AGE_RANGE3":
        url = "https://play.google.com/store/apps/category/FAMILY?age=AGE_RANGE3&hl=en"
    else:
        url = "https://play.google.com/store/apps/category/"+slug[0].link+"?hl=en"

    title = None

    if post[0].version == "varies_with_device":
        title = "Download "+post[0].title+" For Android - Apps on "+settings.APP_NAME
    else:
        title = "Download "+post[0].title+" "+post[0].version+" For Android - Apps on "+settings.APP_NAME

    data = {
        "appName": settings.APP_NAME,
        "appTitle": title,
        "name": "apps",
        "post": post,
        "details": apps_details,
        "screenshot": apps_ss[0].image.split(','),
        "additional": apps_additional[0].name.split(','),
        "subcategory": SubCategory.objects.all().filter(id_subcategory=1),
        "sidebar": "./sidebars/sidebar_apps.html",
        "current_url": request.build_absolute_uri,
        "array": scraping(url),
    }

    return render_to_response("posts/post_apps.html",data)
