from .models import Listing, Bid


def current_price(listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing)

    return (
        listing.starting_bid
        if len(bids) == 0
        else bids.order_by("-amount").first().amount
    )
