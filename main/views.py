from django.shortcuts import redirect, render

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Quote
from .functions import is_valid_password

def home_view(request):
    include_post_quote = True
    quotes = Quote.objects.all().order_by("-created")
    context = {"include_post_quote": include_post_quote, "quotes": quotes}
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
            try:
                user = User.objects.get(username = username)
                error = "User With This Username Already Exists!    "
            except User.DoesNotExist:
                pass

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

@login_required(login_url="login")
def post_quote_view(request):
    action = "Post"
    error = ""

    if request.method == "POST":
        quote = request.POST.get("quote")

        try:
            quote = Quote.objects.create(
                by = request.user,
                quote = quote
            )
            return redirect("home")
        except Exception:
            error = "An Error Occured! Please Try Again!"

    context = {"action": action, "error": error}
    return render(request, "quote_form.html", context)

@login_required(login_url="login")
def update_quote_view(request, quote_id):
    action = "Update"
    error = ""
    
    quote = Quote.objects.get(id = quote_id)

    if request.user != quote.by:
        return redirect("home")
    
    if request.method == "POST":
        updated_quote = request.POST.get("quote")
        quote.quote = updated_quote

        try:
            quote.save()
            return redirect("home")
        except Exception:
            error = "An Error Occured! Please Try Again!"

    context = {"action": action, "error": error, "quote": quote}
    return render(request, "quote_form.html", context)

@login_required(login_url="login")
def update_quote_view(request, quote_id):
    
    quote = Quote.objects.get(id = quote_id)

    item_category = "Quote"
    item = quote.quote

    if request.user != quote.by:
        return redirect("home")
    
    if request.method == "POST":
        quote.delete()
        return redirect("home")

    context = {"item_category": item_category, "item": item}
    return render(request, "delete.html", context)