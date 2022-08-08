from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listing/<str:id>", views.listing_page, name="listing"),
    path("addwatch/<str:id>", views.addwatch, name="addwatch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<str:id>", views.category, name="category"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("comment/<str:id>", views.comment, name="comment"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
