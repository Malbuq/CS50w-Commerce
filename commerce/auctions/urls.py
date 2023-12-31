from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createListing", views.createListing, name="createListing"),
    path("viewWatchlist", views.viewWatchlist, name="viewWatchlist"),
    path("viewCategories", views.viewCategories, name="viewCategories"),
    path("desactiveListing", views.desactiveListing, name="desactiveListing"),
    path("viewCategory/<int:categoryId>", views.viewCategory, name="viewCategory"),
    path("listings/<int:listingId>", views.viewListing, name="viewListing"),
    path("listings/<int:listingId>/makeBid", views.makeBid, name="makeBid"),
    path("listings/<int:listingId>/addWatchlist", views.addWatchlist, name="addWatchlist"),
    path("listings/<int:listingId>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("listings/<int:listingId>/makeComment", views.makeComment, name="makeComment"),
]
