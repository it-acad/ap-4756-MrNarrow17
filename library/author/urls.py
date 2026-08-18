from django.urls import path
from . import views

app_name = "author"

urlpatterns = [
    path('list/', views.author_list, name="list"),
    path('create/', views.author_create, name="create"),
    path('delete/<int:id>', views.author_delete, name="delete"),
    # path('books/<int:id>', views.author_books, name='books')
]