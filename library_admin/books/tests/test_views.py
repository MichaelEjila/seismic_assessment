from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Book

class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "admin@example.com",
            "first_name": "Admin",
            "last_name": "User"
        }
        self.user = CustomUser.objects.create(**self.user_data)

    def test_list_users_with_borrowed_books(self):
        response = self.client.get(reverse('user-list_users_with_borrowed_books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class BookAPITests(APITestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Author Name",
            "publisher": "Publisher Name",
            "category": "Fiction",
            "status": "available"
        }
        self.user = CustomUser.objects.create(email="admin@example.com", first_name="Admin", last_name="User")

    def test_add_book(self):
        response = self.client.post(reverse('book-list'), self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_unavailable_books(self):
        self.client.post(reverse('book-list'), self.book_data)
        self.client.post(reverse('book-borrow'), {
            "email": self.user.email,
            "book_id": 1,
            "days": 7
        })
        response = self.client.get(reverse('book-unavailable_books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
