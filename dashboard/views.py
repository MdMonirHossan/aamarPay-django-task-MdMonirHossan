# Django imports
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import auth, User
# Project app imports
from payment.models import PaymentTransaction, FileUpload
from activity_log.models import ActivityLog
from payment.celery_task import process_file_word_count
from payment.utils import get_latest_payment

# Create your views here.
@login_required(login_url='/login')
def dashboard(request):
    """
    This function is responsible for rendering dashboard UI and additional logic.

    Returns:
        render: dashboard.html
    """
    user_files = FileUpload.objects.filter(user=request.user)
    payment_history = PaymentTransaction.objects.filter(user=request.user)
    activity_log = ActivityLog.objects.filter(user=request.user)

    # Check for payment eligibility
    latest_payment = get_latest_payment(request)

    can_upload = True if latest_payment else False

    # Template contexts
    context = {
        'title': 'Dashboard',
        'files': user_files,
        'payments': payment_history,
        'logs': activity_log,
        'can_upload': can_upload
    }
    print('------- can upload ---- ', can_upload)
    return render(request, 'dashboard.html', context)


def upload_file(request):
    """
    This function is handling file upload functionality from dashboard

    Returns:
        redirect: /dashboard
    """
    if request.method == 'POST':
        file = request.FILES.get('file')

        if not file:
            messages.warning(request, "Please select a file to upload")
            return redirect('dashboard')

        # Check for payment eligibility
        latest_payment = get_latest_payment(request)

        # redirect to dashboard if there is no successful payment
        if not latest_payment:
            messages.error(request, "You must complete a payment before uploading file.")
            return redirect('dashboard')
        
        # Validate file extension
        extension = file.name.split('.')[-1].lower()
        if extension not in ['txt', 'docx']:
            messages.error(request, "Invalid file type. Allowed only .txt & .docs file.")
            return redirect('dashboard')
        
        # File name
        filename =  file.name.split('.')[0]

        # validate and save file record 
        upload_file = FileUpload.objects.create(
            user = request.user,
            file = file,
            filename = filename,
            upload_time = timezone.now()
        )

        # Make payment as used
        latest_payment.can_upload_file = False
        latest_payment.save()

        messages.success(request, f"File '{file.name}' uploaded successfully.")

        try:
            # Create activity log for file upload
            metadata = {
                "status" : upload_file.status,
                "upload_time" : str(upload_file.upload_time),
                "filename" : file.name,
                "file_size": file.size,
                "content_type": file.content_type,
            }

            # Create activity log for file upload
            ActivityLog.objects.create(
                user = request.user,
                action = 'File Upload',
                description = f"File {filename} uploaded after successful payment.",
                metadata = metadata
            )
        except:
            pass

        # Trigger celery task for word count in the background
        process_file_word_count.delay(upload_file.id)

    return redirect('dashboard')


def signup(request):
    """
    This function is responsible to register a new user to the system.

    Returns:
        render: signup.html
    """
    if request.method == 'GET':
        # check for user is already logged in
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('dashboard')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_pass = request.POST['re-password']
        if password == re_pass:
            # Create new user
            user , created = User.objects.get_or_create(username=username)
            user.email = email
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            messages.warning(request, "Password doesn't match!")
    context = {
        'title': 'Sign Up',
    }
    return render(request, 'signup.html', context)


def login(request):
    """
    This function is responsible for handling login functionality.

    Returns:
        render: login.html
    """
    if request.method == 'GET':
        # check for user is already logged in
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('dashboard')
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        # authenticate user with credentials
        user = auth.authenticate(username=user_name, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Log in Successful')
            return redirect('dashboard')
        else:
            messages.warning(request, 'No user found')
    context = {
        'title': 'Sign In',
    }
    return render(request, 'login.html', context)

def log_out(request):
    """
    This function is responsible for handling user log out functionality.
    """
    if request.user.is_authenticated:
        auth.logout(request)
        context = {}
        messages.success(request, 'Successfully logged out.')
        return render(request, 'login.html', context)
    return redirect('login')