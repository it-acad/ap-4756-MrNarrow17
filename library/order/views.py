import random
from datetime import timedelta

from book.models import Book
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Order


def is_admin(user: User) -> bool:
    if user.is_authenticated and user.is_staff:
        return True
    raise PermissionDenied


@user_passes_test(is_admin)
def all_orders(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.select_related("user", "book").all().order_by("-created_at")
    return render(request, "order_list.html", {"orders": orders})


@login_required
def my_orders(request: HttpRequest) -> HttpResponse:
    orders = (
        Order.objects.filter(user=request.user)
        .select_related("book")
        .order_by("-created_at")
    )
    return render(request, "my_orders.html", {"orders": orders})


@login_required
def create_order(request: HttpRequest, book_id: int | None = None) -> HttpResponse:
    if request.method == "POST":
        selected_book_id = request.POST.get("book_id") or book_id
        book = get_object_or_404(Book, pk=selected_book_id)

        plated_end_at = timezone.now() + timedelta(days=random.randint(7, 21))

        new_order = Order.create(
            user=request.user, book=book, plated_end_at=plated_end_at
        )

        if new_order:
            messages.success(request, f'Order for "{book.name}" created successfully!')
            return redirect("order:my_orders")
        else:
            messages.error(
                request,
                "Unable to create order. The book might be out of stock or unavailable.",
            )
            return redirect("book:book_list")

    books = Book.objects.filter(count__gt=0)
    selected_book = get_object_or_404(Book, pk=book_id) if book_id else None
    return render(
        request,
        "order_create.html",
        {"books": books, "selected_book": selected_book},
    )


@user_passes_test(is_admin)
def close_order(request: HttpRequest, order_id: int) -> HttpResponse:
    if request.method == "POST":
        order = get_object_or_404(Order, pk=order_id)
        if not order.end_at:
            order.update(end_at=timezone.now())
            messages.success(request, f"Order #{order.id} has been closed.")
        else:
            messages.warning(request, f"Order #{order.id} is already closed.")
    return redirect("order:all_orders")
