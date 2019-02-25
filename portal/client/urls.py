
from django.conf.urls import include, url
from django.urls import path
from client import views

app_name = 'client'
urlpatterns = [
    path('', views.direct),
    path('home', views.home, name='home'),
    path('setup', views.setup, name='setup'),
    path('checkout', views.checkout, name='checkout'),
    path('login/', views.user_login, name='login'),
    # Dữ liệu các quốc gia và region dạng json
    path('json-nations-states', views.nations_states),
    # Dữ liệu timezone dạng json
    path('timezone', views.timezone),
    path('logout', views.user_logout, name='logout'),
    # Kích hoạt tài khoản email
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    # Đặt lại mật khẩu
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.resetpwd, name='resetpassword'),
    # Dữ liệu người dùng hiện tại dạng json
    path('data-user-json', views.data_user_json)
]