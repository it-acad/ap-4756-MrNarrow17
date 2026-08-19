from book.models import Book
from django.contrib import admin

from .models import Author


class BookInline(admin.TabularInline):
    model = Book.authors.through
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "surname", "name", "patronymic")
    search_fields = ("name", "surname", "patronymic")
    inlines = [BookInline]

    fieldsets = (("Author Details", {"fields": ("surname", "name", "patronymic")}),)
