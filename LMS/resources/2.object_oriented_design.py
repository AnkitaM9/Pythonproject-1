from datetime import datetime, timedelta
from functools import wraps

def display_quote():
    quote="“ A room without books is like a body without a soul.” - Marcus Tullius Cicero "
    print(f"\n*** Motivational Quote ***\n{quote}\n")

# using decorator to log actions performed by members
def log_action(action): 
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            print(f"\nAction: {action} - {self.member_name}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

# using decorator to check if books available in the libraray before borrowing or returning
def check_book_in_the_library(func):
    @wraps(func)
    def wrapper(self, isbn, *args ,**kwargs):
        book=self.find_book(isbn)
        if not book:
            print(f" Book with ISBN {isbn} not found in the Library")
            return
        return func(self, isbn, *args ,**kwargs)
    return wrapper

# class book with class attribute and class method
class Book:
    total_books_in_library=0 # this attribute to keep track of the total number

    def __init__(self, title, author ,isbn):
        self.title=title
        self.author=author
        self.isbn=isbn
        self.is_issued=False
        self.due_date=None
        Book.total_books_in_library +=1

    @classmethod
    def total_books(cls):
        return f"total books in the Library {cls.total_books_in_library}"
    def __str__(self):
        status = "Available" if not self.is_issued else f"Issued, Due Date: {self.due_date}"
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {status}"



class Library:
    issued_books_count=0

    def __init__(self):
        self.books =[]
    def add_book(self,book):
        self.books.append(book)
        print(f"Book '{book.title}' added to the Library")

    def display_books(self):
        if not self.books:
            print("No books in the library.")
        else :
            for book in self.books:
                print(book)
    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
             return book
        return None
    
    def issue_book(self, isbn):
        book = self.find_book(isbn)
        if book and not book.is_issued:
            book.is_issued = True
            book.due_date = datetime.now() + timedelta(days=14) # Set due date to 14 days from now
            Library.issued_books_count += 1  # Increment class attribute for issued books
            print(f"Book '{book.title}' issued. Due date: {book.due_date.strftime('%Y-%m-%d')}.")
        elif book and book.is_issued:
            print(f"Book '{book.title}' is already issued.")

    def return_book(self, isbn):
        book=self.find_book(isbn)
        if book and book.is_issued:
            book.is_issued = False
            book.due_date = None  # Clear due date on return
            Library.issued_books_count -= 1 # Decrement class attribute for issued books
            print(f"Book '{book.title}' returned.")
        elif book and not book.is_issued:
            print(f"Book '{book.title}' was not issued.")      

    @classmethod
    def total_issued_books(cls):
        return f"Total issued books: {cls.issued_books_count}"
    
# Derived class for Library Members with class attributes and methods
class Member(Library):
    members_count = 0  # Class attribute to track number of members

    def __init__(self, member_name):
        super().__init__()
        self.member_name=member_name
        self.borrowed_books = []
        Member.members_count += 1  # Increment the number of members

    @classmethod
    def total_members(cls):
        return f"Total members: {cls.members_count}"
    
    @log_action("Borrow Book")
    @check_book_in_the_library
    def borrow_book(self, isbn):
        book=self.find_book(isbn)
        if book and not book.is_issued:
            self.issue_book(isbn)
            self.borrowed_books.append(book)
            print(f"{self.member_name} borrowed '{book.title}'.")
        else:
            print(f"{self.member_name} cant borrow the book with ISBN {isbn}.")
    
    @log_action("Return Book")
    @check_book_in_the_library
    def return_borrowed_book(self, isbn):
        book = self.find_book(isbn)
        if book in self.borrowed_books:
            self.return_book(isbn)
            self.borrowed_books.remove(book)
            print(f"{self.member_name} returned '{book.title}'.")
        else:
            print(f"{self.member_name} does not have the book with ISBN {isbn}.")

    def check_overdue_books(self):
        overdue_books = [book for book in self.borrowed_books if book.due_date and datetime.now()]
        if overdue_books:
            print(f"{self.member_name}, you have the following overdue books :")
            for book in overdue_books:
                print(f"- '{book.title}' (Due Date: {book.due_date.strftime('%Y-%m-%d')})")
        else:
            print(f"{self.member_name}, You have no overdue books.")

display_quote()
library=Library()

# adding books to the Library
library.add_book(Book("The Woman","Kristin Hannah","1011"))
library.add_book(Book("A Gentleman in Moscow","Amor Towles","2011"))
library.add_book(Book("Kafka on the Shore","Haruki Murakami","3011"))


#Display all books
print("\nLibrary books:")
library.display_books() 

# creating a Library member
member=Member("Ankita M")

#Borrowing a book
print("\nBorrowing a book:")
member.add_book(Book("A Gentleman in Moscow","Amor Towles","2011"))
member.borrow_book("2011")

#check overdue books
member.check_overdue_books()

#simulate passing of time 
for book in member.borrowed_books:
    book.due_date=datetime.now() - timedelta(days=1)

member.check_overdue_books()

#returning the book
print("\nReturnig the book:")
member.return_borrowed_book("2011")

print("\n" + Library.total_issued_books())
print("\n" + Member.total_members())
print("\nLibrary books after return :")
library.display_books()
