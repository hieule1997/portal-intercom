from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    # path('', views.user_login),
    path('', views.home, name='home'),
]