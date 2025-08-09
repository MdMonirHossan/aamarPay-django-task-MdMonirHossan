from django.urls import path
from .views import ActivityLogListView

# All urls for this app
urlpatterns = [
    path('activity', ActivityLogListView.as_view(), name='activity_logs'),
]