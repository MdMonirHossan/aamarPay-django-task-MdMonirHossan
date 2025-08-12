from django.urls import path
from .views import dashboard, signup, login, upload_file, log_out

urlpatterns = [
    # Dashboard url
    path('', dashboard, name='dashboard'),
    path('dashboard', dashboard, name='dashboard'),

    # Url for uploading file for dashboard
    path('upload-file', upload_file, name='upload_file' ),

    # User authentication urls
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', log_out, name='logout')
]