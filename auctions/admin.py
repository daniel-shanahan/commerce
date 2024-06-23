from django.contrib import admin

from .models import Listing, User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email")


admin.site.register(Listing)
admin.site.register(User, UserAdmin)
