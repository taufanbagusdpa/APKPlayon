from django.urls import path
from movies import views

urlpatterns = [
    path('top', views.top, name='moviestop'),
    path('new', views.new, name='moviesnew'),
]
