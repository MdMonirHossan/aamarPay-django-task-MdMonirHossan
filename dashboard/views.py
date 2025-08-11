from django.shortcuts import render
from payment.models import PaymentTransaction, FileUpload
from activity_log.models import ActivityLog

# Create your views here.

def dashboard(request):
    user_files = FileUpload.objects.all()
    context = {
        'title': 'Dashboard',
        'files': user_files
    }
    return render(request, 'dashboard.html', context)