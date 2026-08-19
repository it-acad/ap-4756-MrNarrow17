from author.models import Author
from django.contrib import admin

from .models import Order


class OrderAuthorListFilter(admin.SimpleListFilter):
    title = "author"
    parameter_name = "author_id"

    def lookups(self, request, model_admin):
        return [
            (
                author.id,
                f"{author.name} {author.surname}".strip() or f"Author #{author.id}",
            )
            for author in Author.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(book__authors__id=self.value())
        return queryset


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_user",
        "get_book",
        "created_at",
        "plated_end_at",
        "end_at",
    )

    list_filter = (
        "book__id",
        "book__name",
        OrderAuthorListFilter,
        "created_at",
        "end_at",
    )
    search_fields = ("id", "user__email", "book__name", "book__authors__surname")
    raw_id_fields = ("user", "book")

    fieldsets = (
        ("Order Assignment", {"fields": ("user", "book")}),
        (
            "Issue & Return Timelines",
            {
                "fields": ("plated_end_at", "end_at"),
                "description": "Track date of issue and book return status.",
            },
        ),
    )

    @admin.display(description="User")
    def get_user(self, obj):
        if obj.user:
            return obj.user.email or f"User #{obj.user.id}"
        return "-"

    @admin.display(description="Book")
    def get_book(self, obj):
        if obj.book:
            return obj.book.name or f"Book #{obj.book.id}"
        return "-"
