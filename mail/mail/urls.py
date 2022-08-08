from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("compose", views.compose, name="compose"),
    path("email/<int:email_id>", views.email, name="email"),
    path("mailbox/<str:mailbox>", views.mailbox, name="mailbox"),
]
