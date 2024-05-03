from django.urls import path
from . import views

urlpatterns= [
    path('', views.home, name='home'),  # URL for the home page
    ]