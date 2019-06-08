from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime

class posts(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    slug = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()
    view = models.IntegerField()
    updated_at = models.DateTimeField(default=datetime.datetime.now())
    created_at = models.DateTimeField(default=datetime.datetime.now())

    def __str__(self):
        return '%s %s %s %s %s %s %s %s' % (self.id.pk, self.slug, self.image, self.title, self.content, self.view, self.updated_at, self.created_at)

    def __unicode__(self):
        return self.id

    def get_absolute_url(self):
        return "/movies/%s/%s" % (self.id, self.slug)

class details(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    star = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    rating = models.CharField(max_length=50)
    release = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    video = models.CharField(max_length=255)

    def __str__(self):
        return '%s %s %s %s %s %s %s' % (self.id_posts.pk,self.star,self.genre,self.rating,self.release,self.duration,self.video)

class actor(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

    def __str__(self):
        return '%s %s' % (self.id_posts.pk, self.name)

class producer(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

class director(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

class writer(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

class additional(models.Model):
    id_posts = models.ForeignKey(posts, on_delete=models.SET_NULL, null=True)
    name = models.TextField()

    def __str__(self):
        return '%s' % (self.name)
