from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing
from .forms import ListingForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)

    return render(request, "auctions/listing.html", {"listing": listing})


@login_required
def new(request):
    if request.method == "POST":
        listing = ListingForm(request.POST)
        if not listing.is_valid():
            return (render, request, "auctions/new.html", {"form": listing})
        elif Decimal(request.POST["starting_bid"]) <= 0:
            return render(
                request,
                "auctions/new.html",
                {"form": listing, "message": "Starting bid must be greater than zero."},
            )
        else:
            listing = listing.save(commit=False)
            listing.created_by = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/new.html", {"form": ListingForm()})


def categories(request):
    categories = {}
    for key, category in Listing.CATEGORY_CHOICES.items():
        categories[category] = Listing.objects.filter(category=key).count()
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category):
    category_key = list(Listing.CATEGORY_CHOICES.keys())[
        list(Listing.CATEGORY_CHOICES.values()).index(category)
    ]
    listings = Listing.objects.filter(category=category_key)
    return render(
        request, "auctions/category.html", {"category": category, "listings": listings}
    )
