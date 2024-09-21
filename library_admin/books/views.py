from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import CustomUser as User, Book
from .serializers import BookSerializer, UserSerializer
from .rabbitmq import send_book_added_message

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # Custom endpoint to list users and their borrowed books
    @action(detail=False, methods=['get'], url_path='list_users_with_borrowed_books')
    def list_users_with_borrowed_books(self, request):
        users_with_borrowed_books = []
        users = User.objects.all()

        for user in users:
            borrowed_books = Book.objects.filter(borrowed_by=user)
            borrowed_books_data = BookSerializer(borrowed_books, many=True).data
            users_with_borrowed_books.append({
                'user': UserSerializer(user).data,
                'borrowed_books': borrowed_books_data,
            })
        
        return Response(users_with_borrowed_books)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send message to RabbitMQ
        book_data = {
            "title": serializer.instance.title,
            "author": serializer.instance.author,
            "publisher": serializer.instance.publisher,
            "category": serializer.instance.category,
        }
        send_book_added_message(book_data)

        return Response({"success":True, "data":serializer.data})

    # Endpoint to list unavailable books
    @action(detail=False, methods=['get'], url_path='unavailable_books')
    def list_unavailable_books(self, request):
        if Book.objects.filter(status='borrowed').exists():
            unavailable_books = Book.objects.filter(status='borrowed')
            serializer = self.get_serializer(unavailable_books, many=True)
            return Response(serializer.data)
        else:
            return Response({"success":False, "message":"There are currently no borrowed books"})
