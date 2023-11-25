from django.urls import path

from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("quotes/post", views.post_quote_view, name="post_quote"),
    path("quotes/update/<str:quote_id>", views.update_quote_view, name="update_quote"),
    path("quotes/delete/<str:quote_id>", views.update_quote_view, name="delete_quote"),
]