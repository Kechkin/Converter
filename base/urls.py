from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_ui, name='add'),
    path('api/add/', views.api_add, name='api_add'),
    path('api/search/', views.api_search, name='api_search'),
    path('api/convert/', views.api_convert, name='api_convert'),
    path('average_value/', views.average_value, name='average_value'),
    path('search/', views.search_ui, name='search'),
    path('convert/', views.convert_ui, name='convert'),
    path('login/', views.user_login, name="login"),
    path('register/', views.register_page, name="register"),
]
