from django.urls import path
from .views import UserRegistrationView

# All urls for this app
urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user_registration')
]