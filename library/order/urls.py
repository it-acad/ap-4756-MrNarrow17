from django.urls import path

from . import views

app_name = "order"

urlpatterns = [
    path("", views.my_orders, name="my_orders"),
    path("all/", views.all_orders, name="all_orders"),
    path("create/", views.create_order, name="create_order"),
    path(
        "create/<int:book_id>/",
        views.create_order,
        name="create_order_for_book",
    ),
    path("<int:order_id>/close/", views.close_order, name="close_order"),
]
