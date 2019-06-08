from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
from apps.models import *

class Categories(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    id_subcategory = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return "/%s/category/%s" % (self.id_subcategory, self.link)

class posts(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    slug = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    version = models.CharField(max_length=25)
    view = models.IntegerField()
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '%s %s %s %s %s %s %s %s %s' % (self.id.pk, self.slug, self.image, self.title, self.content, self.version, self.view, self.updated_at, self.created_at)

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return "/apps/%s/%s" % (self.version, self.id)

class details(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    developer = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)

    def __str__(self):
        return '%s %s %s %s' % (self.id_posts.pk, self.developer, self.category, self.rating)

class screenshot(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    image = models.TextField()

    def __str__(self):
        return '%s %s' % (self.id_posts.pk, self.image)

class additional(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

    def __str__(self):
        return '%s' % (self.name)

class keywords(models.Model):
    id = models.AutoField(primary_key=True)
    query = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    view = models.IntegerField()
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    created_at = models.DateTimeField(default=datetime.datetime.now())
