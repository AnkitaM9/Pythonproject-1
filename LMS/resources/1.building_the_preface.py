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
