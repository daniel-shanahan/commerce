from django.contrib import admin

from .models import Listing, User, Bid, Comment


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")
    filter_horizontal = ("watchlist",)


admin.site.register(Listing)
admin.site.register(User, UserAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
