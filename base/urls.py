from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('search/', views.search, name='search'),
    path('convert/', views.convert, name='convert'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register_page, name="register"),
]
