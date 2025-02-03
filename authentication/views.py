import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from dashboard.views import dashboard

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # Validation checks
        if not (1 <= len(username) <= 10):
            messages.error(request, 'Username must be between 1 and 10 characters')
            return redirect('signup')
        if password != password2:
            messages.error(request, 'Passwords must match')
            return redirect('signup')

        # Create User
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        # Generate a unique Base32 secret for the user
        base32_secret = pyotp.random_base32()
        user_profile = UserProfile(user=user, base32_secret=base32_secret)
        user_profile.save()

        # Generate OTP and print it to console for testing
        totp1 = pyotp.TOTP(base32_secret)
        otp = totp1.now()
        user_profile.otp = otp
        user_profile.otp_generated_time = timezone.now()
        user_profile.save()

        print(f"Generated OTP for {email} (Signup): {otp}")  # Console output for testing
        
        request.session['username'] = username
        messages.success(request, 'Account created. Please enter the OTP sent to your email (console for now).')
        return redirect('otp_verify_signup')
    
    return render(request, 'authenticate/signup.html')

def otp_verify_signup(request):
    username = request.session.get('username')
    if not username:
        return redirect('signup')
    
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == user_profile.otp and (timezone.now() - user_profile.otp_generated_time).seconds < 30:
            login(request, user)
            messages.success(request, 'Account verified successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid or expired OTP')
            return redirect('otp_verify_signup')
    
    return render(request, 'authenticate/otp_verify_signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Get username from POST data
        password = request.POST.get('password')  # Get password from POST data
        
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)  # Attempt to get the UserProfile
            except UserProfile.DoesNotExist:
                messages.error(request, 'UserProfile does not exist. Please sign up.')
                return redirect('signup')  # Redirect to signup if UserProfile doesn't exist
            
            # If UserProfile exists, generate OTP and process as before
            totp2 = pyotp.TOTP(user_profile.base32_secret)
            otp = totp2.now()
            user_profile.otp = otp
            user_profile.otp_generated_time = timezone.now()
            user_profile.save()

            print(f"Generated OTP for {username} (Login): {otp}")  # Console output for testing
            
            request.session['username'] = username
            messages.info(request, 'Please enter the OTP sent to your email (console for now).')
            return redirect('otp_verify_signin')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
    
    return render(request, 'authenticate/login.html')

def otp_verify_signin(request):
    username = request.session.get('username')
    if not username:
        return redirect('signin')
    
    user = User.objects.get(username=username)
    user_profile = UserProfile.objects.get(user=user)
    
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == user_profile.otp and (timezone.now() - user_profile.otp_generated_time).seconds < 30:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid or expired OTP')
            return redirect('otp_verify_signin')
    
    return render(request, 'authenticate/otp_verify_signin.html')

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Loggedout Sucessfully')
    return redirect('signin')