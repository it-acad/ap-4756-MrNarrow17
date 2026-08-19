from author.models import Author
from django.contrib import admin

from .models import Book


class AuthorListFilter(admin.SimpleListFilter):
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
            return queryset.filter(authors__id=self.value())
        return queryset


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "get_authors", "count")
    list_filter = (AuthorListFilter, "count")
    search_fields = ("id", "name", "authors__name", "authors__surname")
    filter_horizontal = ("authors",)

    @admin.display(description="Authors")
    def get_authors(self, obj):
        return ", ".join([f"{a.name} {a.surname}" for a in obj.authors.all()])
