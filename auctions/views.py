from decimal import Decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Bid
from .forms import ListingForm, BidForm
from .utils import listings_with_current_price


def index(request):
    listings = listings_with_current_price(Listing.objects.all())

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
    bids = Bid.objects.filter(listing=listing)

    # Set initial bid values
    num_bids = len(bids)
    current_price = listing.starting_bid
    leading_bidder = False

    # Update bid values
    if num_bids > 0:
        highest_bid = bids.order_by("-amount").first()
        current_price = highest_bid.amount
        if highest_bid.created_by.id == request.user.id:
            leading_bidder = True

    # Set context for template
    context = {
        "listing": listing,
        "num_bids": num_bids,
        "current_price": current_price,
        "leading_bidder": leading_bidder,
        "bid_form": BidForm(),
    }

    if request.method == "POST":
        if request.POST["form_type"] == "bid":
            # Bid
            bid_form = BidForm(request.POST)
            if not bid_form.is_valid():
                # Invalid bid form
                context["bid_form"] = bid_form
                return render(request, "auctions/listing.html", context)
            else:
                minimum_bid = (
                    current_price
                    if num_bids == 0
                    else current_price + round(Decimal(0.01), 2)
                )
                if bid_form.cleaned_data["amount"] < minimum_bid:
                    # Bid amount below minimum
                    context["bid_form"] = bid_form
                    context["bid_message"] = f"Bid must be at least ${minimum_bid}."
                    return render(request, "auctions/listing.html", context)
                else:
                    # Successful bid
                    bid = bid_form.save(commit=False)
                    bid.created_by = request.user
                    bid.listing = listing
                    bid.save()
                    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    return render(request, "auctions/listing.html", context)


@login_required
def new(request):
    if request.method == "POST":
        listing = ListingForm(request.POST)
        if not listing.is_valid():
            return render(request, "auctions/new.html", {"form": listing})
        elif Decimal(listing.cleaned_data["starting_bid"]) <= 0:
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
    listings = listings_with_current_price(
        Listing.objects.filter(category=category_key)
    )
    return render(
        request, "auctions/category.html", {"category": category, "listings": listings}
    )
