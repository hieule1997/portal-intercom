
from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'client'
urlpatterns = [
    path('', views.home, name='home'),
    path('setup', views.setup, name='setup'),
    path('checkout', views.checkout, name='checkout'),
]