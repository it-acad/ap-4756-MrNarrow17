from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CustomUser

admin.site.unregister(Group)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "is_active",
    )
    list_filter = ("role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("id",)

    fieldsets = (
        ("Credentials", {"fields": ("email", "password")}),
        (
            "Personal Information",
            {"fields": ("first_name", "middle_name", "last_name")},
        ),
        (
            "Permissions & Roles",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
