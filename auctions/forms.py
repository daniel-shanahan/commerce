from django.forms import ModelForm, Textarea

from .models import Listing


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
