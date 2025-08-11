from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
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

def signup(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('dashboard')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_pass = request.POST['re-password']
        if password == re_pass:
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
    if request.method == 'GET':
        if request.user.is_authenticated:
            messages.warning(request, 'You are already logged in')
            return redirect('/')
    if request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
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