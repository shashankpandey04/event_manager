from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from accounts.utils.email import send_welcome_mail

def register_view(request):

    if request.method == "POST":
        full_name = request.POST.get("fullName")
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phoneNumber")
        dob = request.POST.get("dateOfBirth")
        role = request.POST.get("role", "participant")

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirmPassword")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        user.fullName = full_name
        user.phoneNumber = phone
        user.dateOfBirth = dob
        user.role = role
        user.save()

        # send_welcome_mail(user)

        login(request, user)

        return redirect("dashboard")

    return render(request, "accounts/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)

            return redirect("dashboard")
        
    return render(request, "accounts/login.html")

@login_required(login_url="/auth/login")
def logout_view(request):
    logout(request)
    return redirect("login")