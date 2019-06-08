from django.urls import path
from books import views

urlpatterns = [
    path('top', views.top, name='bookstop'),
    path('new', views.new, name='booksnew'),
]
