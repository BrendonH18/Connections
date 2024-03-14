from django.urls import path, include
from .views import register_user, login

urlpatterns = [
    path('register/', register_user, name="register"),
    path('login/', login, name="login")
]