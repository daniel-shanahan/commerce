from django.forms import ModelForm, Textarea

from .models import Listing, Bid, Comment


class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "image_url", "category"]
        widgets = {
            "description": Textarea(
                attrs={"cols": 50, "rows": 2, "class": "form-control mb-3"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control mb-3"})
        self.fields["starting_bid"].widget.attrs.update({"class": "form-control mb-3"})
        self.fields["image_url"].widget.attrs.update({"class": "form-control mb-3"})
        self.fields["category"].widget.attrs.update({"class": "form-control mb-3"})


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "$100.00"}
        )
        self.fields["amount"].label = "Bid Amount"


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        widgets = {
            "text": Textarea(
                attrs={"cols": 50, "rows": 2, "class": "form-control mb-3"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = "Add a Comment"
