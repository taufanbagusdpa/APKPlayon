from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from . import views as homeviews
from apps import views as appsviews
from movies import views as moviesviews
from books import views as booksviews
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .sitemaps import *
from django.contrib.sitemaps import views

sitemaps = {
    'pages': PagesSitemap,
    'categories': CategoriesSitemap,
    'subcategory': SubCategorySitemap,
    'apps-posts': AppsPostsSitemap,
    'movies-posts': MoviesPostsSitemap,
    'books-posts': BooksPostsSitemap,
}

extra_patterns = [
    path('about-us', homeviews.pages, name="about-us"),
    path('contact-us', homeviews.pages, name="contact-us"),
    path('DMCA', homeviews.pages, name="DMCA"),
]

urlpatterns = [
    path('', homeviews.index, name='main'),
    path('post', homeviews.post),
    url(r'^store/(?P<search>[-\w\d]+)', homeviews.search),
    path('page/', include(extra_patterns)),
    path('apps/', appsviews.index, name='apps'),
    path('apps/', include('apps.urls')),
    path('movies/', moviesviews.index, name='movies'),
    path('movies/', include('movies.urls')),
    path('books/', booksviews.index, name='books'),
    path('books/', include('books.urls')),
    path('generate/<url>', appsviews.generate),
    path('apps/', include([
        url(r'^details/(?P<slug_posts>[-\w\d]+)', appsviews.details_posts),
        path('category/<slug>', appsviews.category, name="appsubcategory"),
        path('<version>/<id>', appsviews.appsposts),
        path('download/<server>/<version>/<id>', appsviews.download),
    ])),
    path('movies/', include([
        url(r'^details/(?P<slug_posts>[-\w\d]+)', moviesviews.details_posts),
        path('category/<slug>', moviesviews.category),
        path('<id>/<slug>', moviesviews.moviesposts),
        path('download/<server>/<id>', moviesviews.download),
    ])),
    path('books/', include([
        url(r'^details/(?P<slug_posts>[-\w\d]+)', booksviews.details_posts),
        path('category/<slug>', booksviews.category),
        path('<id>/<slug>', booksviews.booksposts),
        path('download/<server>/<id>', booksviews.download),
    ])),
    path('sitemap_index.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

urlpatterns += staticfiles_urlpatterns()
