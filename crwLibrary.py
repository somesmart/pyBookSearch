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
            if book.isbn == isbn:
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

#     def remove_isbn(self, isbn):
#         """
#         Remove all books with the given ISBN from the list
#         managed by this Library.
#         """

#         # Use a list comprehension to modify the book list
#         # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
#         self.book_list[:] = [book for book in self.book_list if book.isbn != isbn]

# ##        for book in self.book_list:
# ##            if book.isbn == isbn:
# ##                self.remove_book(book)

    def read_from_file(self, delimiter):
        """Open the CSV file associated with this Library, and create a
           Book for each book described within."""

        try:
            library_file = open(self.filename, "rt")

            # The first line of the file is to be used for key names
            book_reader = csv.DictReader(library_file, delimiter=delimiter)

            for book in book_reader:
                self.book_list.append(crwBook.new_book(from_dict=book))

            library_file.close()
        except IOError:
            print("### No library file.")

    def save_to_file(self, delimiter):
        library_file = open(self.filename, "wt")
        book_writer = csv.writer(library_file, lineterminator='\n', delimiter=delimiter)

        book_writer.writerow([crwBook.bkFields[crwBook.bkISBN],
                              crwBook.bkFields[crwBook.bkTitle],
                              crwBook.bkFields[crwBook.bkAuthor],
                              crwBook.bkFields[crwBook.bkBinding],
                              crwBook.bkFields[crwBook.bkPublisher],
                              crwBook.bkFields[crwBook.bkPublished],
                              crwBook.bkFields[crwBook.bkUsedPrice]])

        for book in self.book_list:
            isbn = book.isbn
            title = book.title
            author = book.author
            binding = book.binding
            publisher = book.publisher
            published = book.published
            usedPrice = book.usedPrice
            book_writer.writerow(
                [isbn, title, author, binding, publisher, published, usedPrice])

        # Close the library file
        library_file.close()

        print("Saved", self.filename)

if __name__ == "__main__":
    library = Library("library_test.csv")
    library.read_from_file(delimiter)

    library.add_book(crwBook.Book("1234", "title1234", "author1234"))
    library.add_book(crwBook.Book("2345", "title2345", "author2345"))
    library.add_book(crwBook.Book("3456", "title3456", "author3456"))

    # library.remove_isbn("2345")

    library.save_to_file(delimiter)

