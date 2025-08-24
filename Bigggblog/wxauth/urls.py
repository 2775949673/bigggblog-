from django.urls import path
from . import views

app_name = 'wxauth'
urlpatterns = [
    path('login', views.wxlogin, name='login'),
    path('logout', views.wxlogout, name='logout'),
    path('register',views.register, name='register'),
    path('captcha',views.send_email_captcha, name='email_captcha'),
]