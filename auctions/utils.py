from .models import Listing, Bid


def current_price(listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing)

    return (
        listing.starting_bid
        if len(bids) == 0
        else bids.order_by("-amount").first().amount
    )


def listings_with_current_price(listings_without_price):
    listings = [listing for listing in listings_without_price.values()]

    for listing in listings:
        listing["current_price"] = current_price(listing["id"])

    return listings
