#!/usr/bin/env python3
"""Define a Library class to store a list of books."""

import crwBook
import csv

class Library(object):
    """The Library class is responsible for..."""

    def __init__(self, filename):
        """Initialise the book list to an empty list and store the filename."""

        self.book_list = []
        self.filename = filename

    def isbn_exists(self, isbn):
        """Check for the existence of the given ISBN within the list of books."""

        exists = False
        book = None
        for book in self.book_list:
            if book.get_isbn() == isbn:
                exists = True
                break
        return exists, book

    def add_book(self, book):
        """Add a book to the list managed by this Library."""
        self.book_list.append(book)

    def remove_book(self, book):
        """Remove a book from the list managed by this Library."""
        try:
            self.book_list.remove(book)
        except ValueError:
            print("### Could not remove book.")

    def remove_isbn(self, isbn):
        """Remove all books with the given ISBN from the list managed by this Library."""

        # Use a list comprehension to modify the book list
        # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
        self.book_list[:] = [book for book in self.book_list if book.get_isbn() != isbn]

##        for book in self.book_list:
##            if book.get_isbn() == isbn:
##                self.remove_book(book)

    def read_from_file(self):
        """Open the CSV file associated with this Library, and create a Book for
           each book described within."""

        try:
            library_file = open(self.filename, "rt")

            book_reader = csv.DictReader(library_file)

            for book in book_reader:
                isbn = book[crwBook.bkFields[crwBook.bkISBN]]
                title = book[crwBook.bkFields[crwBook.bkTitle]]
                author = book[crwBook.bkFields[crwBook.bkAuthor]]

                new_book = crwBook.Book(isbn, title, author)

                try:
                    new_book.set_binding(book[crwBook.bkFields[crwBook.bkBinding]])
                    new_book.set_publisher(book[crwBook.bkFields[crwBook.bkPublisher]])
                    new_book.set_published(book[crwBook.bkFields[crwBook.bkPublished]])
                except KeyError:
                    print("No optional info")

                self.book_list.append(new_book)

            library_file.close()
        except IOError:
            print("### No library file.")

    def save_to_file(self):
        library_file = open(self.filename, "wt")
        book_writer = csv.writer(library_file)

        book_writer.writerow([crwBook.bkFields[crwBook.bkISBN],
                              crwBook.bkFields[crwBook.bkTitle],
                              crwBook.bkFields[crwBook.bkAuthor],
                              crwBook.bkFields[crwBook.bkBinding],
                              crwBook.bkFields[crwBook.bkPublisher],
                              crwBook.bkFields[crwBook.bkPublished]])

        for book in self.book_list:
            isbn = book.get_isbn()
            title = book.get_title()
            author = book.get_author()
            binding = book.get_binding()
            publisher = book.get_publisher()
            published = book.get_published()
            book_writer.writerow([isbn, title, author, binding, publisher, published])

        # Close the library file
        library_file.close()

        print("Saved", self.filename)

if __name__ == "__main__":
    library = Library("library_test.csv")
    library.read_from_file()

    library.add_book(crwBook.Book("1234", "title1234", "author1234"))
    library.add_book(crwBook.Book("2345", "title2345", "author2345"))
    library.add_book(crwBook.Book("3456", "title3456", "author3456"))

    library.remove_isbn("2345")

    library.save_to_file()

    
