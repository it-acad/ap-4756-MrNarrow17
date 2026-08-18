from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path("list/", views.user_list, name="list"),
    path("<int:id>/", views.user_info, name="user"),
]
