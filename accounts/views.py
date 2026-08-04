from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


def register(request):
    message = ""

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"]
            )

            message = "Registration Successful!"

            return redirect("login")

        else:
            message = "Please correct the errors below."

    else:
        form = RegisterForm()

    return render(request, "register.html", {
        "form": form,
        "message": message
    })
def login_view(request):
    message = ""

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        print("Username:", username)
        print("Password:", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("User:", user)

        if user is not None:
            print("LOGIN SUCCESS")
            login(request, user)

            if user.is_superuser:
                print("ADMIN LOGIN")
                return redirect("dashboard")

            print("USER LOGIN")
            return redirect("report")

        else:
            print("LOGIN FAILED")
            message = "Invalid Username or Password"

    return render(request, "login.html", {
        "message": message
    })

def logout_view(request):

    logout(request)

    return redirect("home")