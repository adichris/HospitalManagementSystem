from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as UserBaseAdmin
from .forms import UserCreationForm, UserChangeForm


@admin.register(User)
class UserModelAdmin(UserBaseAdmin):
    # Form to add and change user instance
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    list_display = ("get_full_name", "phone_number", "gender")
    list_filter = ("is_active", "is_admin", "is_superuser", 'is_online')

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Personal Information", {"fields": ("first_name", "last_name", "dob", "email")}),
        ("Profile Picture", {"fields": ("picture", )}),
        ("Permissions", {"fields": ("is_admin", "is_superuser"), "classes": "wide"}),
        ("Active Status", {"fields": ("is_active", ), "classes": "wide"}),
        ("Groups and Authorization", {"fields": ("groups", ), "classes": "wide"}),
    )
    add_fieldsets = (
        ("Credential", {"fields": ("phone_number", "password", "password_confirmation"), "classes": "wide"}),
        ("Personal Information", {"fields": ("first_name", "last_name", "email", "gender"), "classes": "wide"})
    )

    search_fields = ("email", "first_name", "last_name")
    ordering = ("first_name", "last_name")
    filter_horizontal = ()
