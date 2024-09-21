from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import CustomUser, Book

class UserAPITests(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        }

    def test_enroll_user(self):
        response = self.client.post(reverse('user-list'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        self.client.post(reverse('user-list'), self.user_data)
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class BookAPITests(APITestCase):
    def setUp(self):
        self.book_data = {
            "title": "Test Book",
            "author": "Author Name",
            "publisher": "Publisher Name",
            "category": "Fiction",
            "status": "available"
        }

        self.user = CustomUser.objects.create(**{
            "email": "testuser@example.com",
            "first_name": "Test",
            "last_name": "User"
        })

    def test_create_book(self):
        response = self.client.post(reverse('book-list'), self.book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_available_books(self):
        self.client.post(reverse('book-list'), self.book_data)
        response = self.client.get(reverse('book-available_books'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_borrow_book(self):
        self.client.post(reverse('book-list'), self.book_data)
        response = self.client.post(reverse('book-borrow'), {
            "email": self.user.email,
            "book_id": 1,
            "days": 7
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("success", response.data)
