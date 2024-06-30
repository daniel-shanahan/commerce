from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listings/<int:listing_id>", views.listing, name="listing"),
    path("listings/<int:listing_id>/watch", views.watch, name="watch"),
    path("listings/<int:listing_id>/close", views.close, name="close"),
    path("listings/new", views.new, name="new"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("watchlist", views.watchlist, name="watchlist"),
]
