from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display: tuple[str] = ("full_name", "is_staff", "is_active",)
    list_filter: tuple[str] = ("is_staff", "is_active",)
    fieldsets: tuple = (
        (None, {"fields": ("email", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets: tuple = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "first_name","last_name", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields: tuple = ("email","first_name", "last_name")
    ordering: tuple[str] = ( "first_name",)

    @admin.display(empty_value="N/A", description="Name", ordering="first_name")
    def full_name(self, object):
        return f"{object.first_name} {object.last_name}".title()