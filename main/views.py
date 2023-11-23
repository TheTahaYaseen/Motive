from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .functions import is_valid_password

def home_view(request):
    include_post_quote = True
    context = {"include_post_quote": include_post_quote}
    return render(request, "home.html", context)

def register_view(request):
    action = "Register"
    error = ""

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        fields = [username, password]
        if "" in fields:
            error = "Please Fill Out All The Fields!"

        if not error:
            if not is_valid_password(password)["validity"]:
                error = is_valid_password(password)["error"]

        if not error:
            user = User.objects.create(username=username, password=password)
            login(request, user)
            return redirect("home")

    context = {"action": action, "error": error}
    return render(request, "auth_form.html", context)

def login_view(request):
    action = "Login"
    error = ""

    if request.method == "POST":
        username = request.POST.get("username").lower()
        password = request.POST.get("password")

        fields = [username, password]
        if "" in fields:
            error = "Please Fill Out All The Fields!"

        if not error:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                error = "User Does Not Exist!"

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                previous_page = request.META.get("HTTP_REFERER")
                return redirect(previous_page)
            else:
                error = "An Error Occured Login! Probably An Issue With The Credentials!"

    context = {"action": action, "error": error}
    return render(request, "auth_form.html", context)

def logout_view(request):

    if request.user.is_authenticated:
        logout(request)
    
    previous_page = request.META.get("HTTP_REFERER")
    return redirect(previous_page)