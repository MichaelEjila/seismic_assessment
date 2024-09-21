from books.models import Book
from datetime import timedelta
from django.utils.timezone import now

def borrow_book(user, **kwargs):
    book_id = kwargs.get("book_id")
    book_title = kwargs.get("book_title")
    borrow_days = kwargs.get("days")

    if not borrow_days:
        return {"success": False, "message": 'Number of days not provided'}

    # Retrieve the book based on id or title
    book = Book.objects.filter(id=book_id).first() or Book.objects.filter(title=book_title).first()

    if book:
        if book.status == 'borrowed':
            return {"success": False, "message": "This book is already borrowed."}

        borrowed_until = now() + timedelta(days=int(borrow_days))
        book.status = 'borrowed'
        book.borrowed_by = user
        book.borrowed_until = borrowed_until
        book.save()

        return {"success": True, "message": f"{book.title} successfully lent out to {user.first_name} {user.last_name}"}
    else:
        return {"success": False, "message": "Book does not exist"}
