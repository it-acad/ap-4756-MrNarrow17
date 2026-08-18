from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

User = get_user_model()


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            messages.error(request, "Email and password are required")
            return render(request, "authentication/login.html", {"email": email})

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f"Logged in as {email}")
                return redirect("home")
        except User.DoesNotExist:
            pass

        messages.error(request, "Invalid email or password")
        return render(
            request, "authentication/login.html", {"email": email, "password": password}
        )

    return render(request, "authentication/login.html")


def register_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        extra_fields = {
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "middle_name": request.POST.get("middle_name"),
            "is_active": True,
        }

        if not email or not password:
            messages.error(request, "Email and password are required")
            return render(
                request,
                "authentication/register.html",
                {"email": email, "password": password, **extra_fields},
            )

        if User.objects.filter(email=email).exists():
            messages.error(request, "User already exists")
            return render(
                request,
                "authentication/register.html",
                {"email": email, "password": password, **extra_fields},
            )

        user = User.objects.create_user(email, password, **extra_fields)
        login(request, user)
        messages.success(request, f"Logged in as {email}")
        return redirect("home")

    return render(request, "authentication/register.html")


def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    messages.success(request, f"Logged out")
    return redirect("home")
