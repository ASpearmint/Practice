from django.urls import include, path
from . import views

#Remember to add function names from views.py into here!
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:id>", views.target_page, name="target_page"),
    path("search", views.search, name="search"),
    path("create_page", views.create_page, name="create_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("random_page", views.random_page, name="random_page"),
    
]
