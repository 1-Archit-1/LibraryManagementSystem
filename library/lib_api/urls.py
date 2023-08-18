from django.urls import path, include
from .api import  AddBooks, ReturnBorrowBook, ViewBooks,RemoveBooks,UpdateBooks
urlpatterns = [
    path('api/add-book', AddBooks.as_view()),
    path('api/view-book', ViewBooks.as_view()),
    path('api/remove-book', RemoveBooks.as_view()),
    path('api/return-borrow-book', ReturnBorrowBook.as_view()),
    path('api/update-book', UpdateBooks.as_view())
]