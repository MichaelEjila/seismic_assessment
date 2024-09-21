# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend

from books.services import borrow_book
from .models import CustomUser as User, Book
from .serializers import UserSerializer, BookSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['publisher', 'category']  # Add filtering by publisher and category

    # Endpoint for listing available books
    @action(detail=False, methods=['get'], url_path='available_books')
    def available_books(self, request):
        available_books = Book.objects.filter(status='available')
        serializer = self.get_serializer(available_books, many=True)
        return Response(serializer.data)

   
    @action(detail=False, methods=['post'], url_path='borrow')
    def borrow(self, request):
        users_email = request.data.get('email')
        book_id = request.data.get('book_id')
        book_title = request.data.get('title')
        days = request.data.get('days')

        if User.objects.filter(email=users_email).exists():
            user = User.objects.get(email=users_email)

            if book_id or book_title:
                book_info = {"book_id": book_id, "book_title": book_title, "days": days}
                status = borrow_book(user, **book_info)  
                return Response(status)  
            return Response({"success": False, "message": "No book ID or title sent"})
        else:
            return Response({"success": False, "message": "User's email not found"})
