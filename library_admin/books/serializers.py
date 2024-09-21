from rest_framework import serializers
from .models import CustomUser, Book

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'groups', 'user_permissions']
        read_only_fields = ['groups', 'user_permissions']  # Prevent modification of these fields

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'status', 'borrowed_until', 'borrowed_by']
        read_only_fields = ['borrowed_by']  # Prevent modification of borrowed_by field
