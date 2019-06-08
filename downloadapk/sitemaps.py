from django.contrib import sitemaps
from django.urls import reverse
from apps.models import *
from movies.models import posts as moviespost
from books.models import posts as bookspost

class PagesSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['main','about-us', 'contact-us', 'DMCA']

    def location(self, item):
        return reverse(item)

class CategoriesSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['apps', 'appstop', 'appsnew', 'movies', 'moviestop',
        'moviesnew', 'books', 'bookstop', 'booksnew']

    def location(self, item):
        return reverse(item)

class SubCategorySitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return SubCategory.objects.all()

class AppsPostsSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'always'

    def items(self):
        return posts.objects.order_by('-updated_at').all()[:5000]

    def lastmod(self, obj):
        return obj.created_at

class MoviesPostsSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'always'

    def items(self):
        return moviespost.objects.order_by('-updated_at').all()[:5000]

    def lastmod(self, obj):
        return obj.created_at

class BooksPostsSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = 'always'

    def items(self):
        return bookspost.objects.order_by('-updated_at').all()[:5000]

    def lastmod(self, obj):
        return obj.created_at
