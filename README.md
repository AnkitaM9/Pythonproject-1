## Library Management System in Python 

The Library Management System is a software application designed to streamline library operations such as managing books, tracking members, and handling borrowing and returning processes. This system aims to improve efficiency and enhance user experience for librarians and members.


The objective of this project is to develop a feature-rich Library Management System using Python with a focus on Object-Oriented Programming (OOP) principles such as Inheritance, Decorators, and Class Methods. 

# Features:
Book Management: Add, update, delete, and search books.
Member Management: Register new members, view and update member details.
Borrow and Return: Keep track of issued books, return dates, and overdue fines.
Reports: Generate reports for borrowed books, overdue items, and inventory.
User Roles: Separate access for administrators and library members.



# import the requirements
from datetime import datetime,timedelta
from functools import wraps

#using function to display a motivational quote
def display_quote():
    quote="“ A room without books is like a body without a soul.” - Marcus Tullius Cicero "
    print(f"\n*** Motivational ***\n{quote}\n")

# using decorator to log actions performed by members
def log_action(action): 
    def decorators(func):
        @wraps(func)
        def wrapper(self, *args,**kwargs):
            print(f"\nAction: {action} - {self.member_name}")
            return func (self, *args,**kwargs)
        return wrapper
    return decorators

# using decorator to check if books available in the libraray before borrowing or returning
def check_book_in_the_library(func):
    @wraps(func)
    def wrapper(self, isbn, *args ,**kwargs):
        book=self.find_book(isbn)
        if not book:
            print(f" Book with ISBN {isbn} not found in the Library")
            return func(self, isbn, *args ,**kwargs)
        return wrapper
