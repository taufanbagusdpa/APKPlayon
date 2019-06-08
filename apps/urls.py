from django.urls import path
from apps import views
from downloadapk import views as homeviews

urlpatterns = [
    path('top', views.top, name='appstop'),
    path('new', views.new, name='appsnew'),
]
