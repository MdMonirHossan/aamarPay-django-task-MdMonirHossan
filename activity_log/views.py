from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import ActivityLog
from .serializers import ActivityLogSerializer

# Create your views here.
class ActivityLogListView(generics.ListAPIView):
    """
    This List API view is responsible for providing a list of activity by requested user.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer

    def get_queryset(self):
        '''
        Return a queryset of activities only for the requested user.
        '''
        return ActivityLog.objects.filter(user=self.request.user)
