from django.shortcuts import render

# Create your views here.
def home_view(request):
    include_post_quote = True
    context = {"include_post_quote": include_post_quote}
    return render(request, "home.html", context)