
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("posts", views.posts, name="posts"),
    path("profile/<str:name>", views.profile, name="profile"),
    path("create", views.create_profile, name="create"),
    path("<str:name>/following/<int:page>", views.following, name="following"),
    path("like/<int:id>", views.like, name="like"),
    path("edit/<int:id>", views.edit_post, name="edit"),
]
