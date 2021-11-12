from django.contrib import admin
from django.urls import path
from .views import*

urlpatterns = [
    path('', home,name="home"),
    path('login/', login,name="login"),
    path('register/', register,name="register"),
    path('sucess/', sucess,name="sucess"),
    path('send_mail/', send_mail,name="send_mail"),
     path('verify/<auth_token>' , verify , name="verify"),
    path('error/' , error_page , name="error")
]