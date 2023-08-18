from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import LibPermission
from .serializer import BookSerializer
from .models import Book
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class AddBooks(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,LibPermission, )
    @extend_schema(
        request = BookSerializer,)
    def post(self, request, *args,  **kwargs):
        """Allows librarian to add books"""
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()
        return Response({
            "book": BookSerializer(book).data,
            "message": "Book added Successfully",
        })

class RemoveBooks(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,LibPermission, )
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pk',
                description = 'id of the book to remove',
                required=True,)])
    def delete(self, request):
        """remove books"""
        try:
            book_to_delete =  Book.objects.get(id=request.query_params.get('pk'))
            book_to_delete.delete()

            return Response({
                'message': 'Book Deleted Successfully'
            })
        except Exception as e:
            return Response({'error':'not found'})
class UpdateBooks(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,LibPermission, )
    @extend_schema(
        request = BookSerializer,
        parameters=[
            OpenApiParameter(
                name='pk',
                description = 'id of the book to update'),])
    def put(self, request,):
        """Update a book"""
        try:
            book = Book.objects.get(id =request.query_params.get('pk') )
            serializer = BookSerializer(instance=book,data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                'message': 'Action completed successfully',
                'data': serializer.data
            })
        except Exception as e:
            print(e)
            return Response('error')

class ViewBooks(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pk',
                description = 'id of the book to borrow/return , None to return all books'),])
    def get(self,request):
        """view books"""
        try:

            if request.query_params:
                books = Book.objects.get(id =request.query_params.get('pk') )
                if books:
                    book =BookSerializer(books)
            else:
                books = Book.objects.all()
                if books:
                    book = BookSerializer(books , many =True)

            if books:
                return Response({
                    "book": book.data,
                })
        except Exception as e:
            return Response({'error':'not found'})

class ReturnBorrowBook(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='pk',
                description = 'id of the book to borrow/return',
                required=True,
                type=OpenApiTypes.INT),
            OpenApiParameter(
                name='action',
                description = '1 to return and 2 to borrow',
                type=OpenApiTypes.INT,
                required=True,)])
    def put(self, request,):
        """Borrow or return book according to action flag"""
        try:
            action = int(request.query_params.get('action'))
            book = Book.objects.get(id =request.query_params.get('pk') )
            user_obj = request.user
            if book.status == 'BORROWED' and action == 1 and request.user.id == book.borrowed_by:
                serializer = BookSerializer(instance=book,data={'status':'AVAILABLE', 'borrowed_by':None}, partial=True)

            elif book.status == 'AVAILABLE' and action == 2 :
                serializer = BookSerializer(instance=book,data={'status':'BORROWED','borrowed_by':user_obj.id}, partial=True)

            else:
                return Response({
                'message': 'Action not permitted',
            })
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message': 'Action completed successfully',
                'data': serializer.data
            })
        except Exception as e:
            print(e)
            return Response('error')

