from django.urls import path
from .views import dashboard, signup, login

urlpatterns = [
    path('dashboard', dashboard, name='dashboard'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
]