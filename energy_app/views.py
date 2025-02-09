from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib.auth.hashers import make_password, check_password
from .forms import BankBranchRegistrationForm, ForgotPasswordForm, ResetPasswordForm, LoginForm 
from .models import BankBranch

def generate_otp():
    """Generate a random 6-digit OTP"""
    return random.randint(100000, 999999)

def send_otp_email(otp, email):
    """Send OTP to user's email"""
    subject = 'Your OTP Verification Code'
    message = f'Your OTP is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])

def login_view(request):
    """Login view with proper password authentication"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                branch = BankBranch.objects.get(email=email)
                if check_password(password, branch.password):  # Check hashed password
                    messages.success(request, "Login successful!")
                    request.session['branch_id'] = branch.id  # Store user session
                    return redirect('dashboard')  # Redirect to dashboard
                else:
                    messages.error(request, "Invalid password.")
            except BankBranch.DoesNotExist:
                messages.error(request, "User not found.")
    
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_branch(request):
    """Register new bank branch with OTP verification"""
    if request.method == "POST":
        form = BankBranchRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            branch_name = form.cleaned_data['branch_name']
            contact_number = form.cleaned_data['contact_number']
            password = form.cleaned_data['password']

            # Debug: Print values to confirm data is received
            print(f"Received Data: {email}, {branch_name}, {contact_number}, {password}")

            # Check if email already exists
            if BankBranch.objects.filter(email=email).exists():
                messages.error(request, "Email already registered.")
                return redirect('register')

            # Generate OTP and send email
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['registration_data'] = form.cleaned_data

            # Send OTP to email
            send_otp_email(otp, email)

            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('verify_otp')

    else:
        form = BankBranchRegistrationForm()

    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    """Verify OTP for registration and save user"""
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if str(entered_otp) == str(session_otp):
            # OTP is correct, save the user
            data = request.session.get('registration_data')

            if data:
                # Hash password and save user data to the database
                data['password'] = make_password(data['password'])  # Hash password
                branch = BankBranch.objects.create(**data)
                branch.save()

                messages.success(request, "Registration successful!")
                del request.session['otp']  # Clear OTP session
                del request.session['registration_data']  # Clear registration data session
                return redirect('login')  # Redirect to login page
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'verify_otp.html')

def forgot_password(request):
    """Forgot password - send OTP for reset"""
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            # Check if email exists
            if not BankBranch.objects.filter(email=email).exists():
                messages.error(request, "Email not registered.")
                return redirect('forgot_password')

            # Generate OTP and send email
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['reset_email'] = email
            send_otp_email(otp, email)

            messages.success(request, "OTP sent to your email. Please verify.")
            return redirect('reset_password_otp')
    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request):
    """Reset password after OTP verification"""
    if request.method == "POST":
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            email = request.session.get('reset_email')

            if new_password == confirm_password:
                try:
                    branch = BankBranch.objects.get(email=email)
                    branch.password = make_password(new_password)  # Hash new password
                    branch.save()

                    messages.success(request, "Password reset successful!")
                    del request.session['reset_email']  # Clear reset session data
                    return redirect('login')
                except BankBranch.DoesNotExist:
                    messages.error(request, "User not found.")
            else:
                messages.error(request, "Passwords do not match.")
    
    else:
        form = ResetPasswordForm()

    return render(request, 'reset_password.html', {'form': form})
