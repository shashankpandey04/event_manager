from django.shortcuts import render, redirect, get_object_or_404
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

@login_required(login_url="/auth/login")
def manage_users(request):
    if request.user.role != "organizer":
        messages.error(request, "You do not have permission to manage users.")
        return redirect("dashboard")
    users = User.objects.all()
    return render(request, "accounts/manage_users.html", {"users": users})

@login_required(login_url="/auth/login")
def delete_user(request, user_id):
    if request.user.role != "organizer":
        messages.error(request, "You do not have permission to delete users.")
        return redirect("dashboard")
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted successfully!")
    return redirect("manage_users")

@login_required(login_url="/auth/login")
def edit_user(request, user_id):
    if request.user.role != "organizer":
        messages.error(request, "You do not have permission to edit users.")
        return redirect("dashboard")
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.fullName = request.POST.get("fullName")
        user.phoneNumber = request.POST.get("phoneNumber")
        user.dateOfBirth = request.POST.get("dateOfBirth")
        user.role = request.POST.get("role", "participant")
        user.save()
        messages.success(request, "User updated successfully!")
        return redirect("manage_users")
    return render(request, "accounts/edit_user.html", {"user": user})