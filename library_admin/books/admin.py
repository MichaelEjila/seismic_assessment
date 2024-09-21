from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser, Book

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

# Register the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'category', 'status', 'borrowed_by', 'borrowed_until')
    list_filter = ('status', 'publisher', 'category')
    search_fields = ('title', 'author', 'publisher', 'category')
    ordering = ('title',)

