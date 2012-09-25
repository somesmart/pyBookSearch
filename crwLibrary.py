#!/usr/bin/env python
import crwBook
import csv

class Library(object):
    def __init__(self, filename):
        self.book_list = []
        self.filename = filename

    def isbn_exists(self, isbn):
        exists = False
        book = None
        if type(isbn) == str:
            isbn = unicode(isbn)
        for book in self.book_list:
            if book.get_isbn() == isbn:
                exists = True
                break
        return exists, book

    def add_book(self, book):
        self.book_list.append(book)

    def remove_book(self, book):
        print "remove_book"
        try:
            self.book_list.remove(book)
        except ValueError:
            print "### Could not remove book."

    def remove_isbn(self, isbn):
        if type(isbn) == str:
            isbn = unicode(isbn)
        # Use a list comprehension to modify the book list
        # http://stackoverflow.com/questions/1207406/remove-items-from-a-list-while-iterating-in-python
        self.book_list[:] = [book for book in self.book_list if book.get_isbn() != isbn]
##        for book in self.book_list:
##            if book.get_isbn() == isbn:
##                self.remove_book(book)

    def read_from_file(self):
        try:
            library_file = open(self.filename, "rb")

            book_reader = csv.DictReader(library_file)

            for book in book_reader:
                isbn = book[crwBook.STR_ISBN].decode("iso-8859-1")
                title = book[crwBook.STR_TITLE].decode("iso-8859-1")
                author = book[crwBook.STR_AUTHOR].decode("iso-8859-1")

                self.book_list.append(crwBook.Book(isbn,
                                           title,
                                           author))

            library_file.close()
        except IOError:
            print "### No library file."

    def save_to_file(self):
        library_file = open(self.filename, "wb")
        book_writer = csv.writer(library_file)

        book_writer.writerow([crwBook.STR_ISBN,
                              crwBook.STR_TITLE,
                              crwBook.STR_AUTHOR])

        for book in self.book_list:
            isbn = book.get_isbn().encode("iso-8859-1")
            title = book.get_title().encode("iso-8859-1")
            author = book.get_author().encode("iso-8859-1")
            book_writer.writerow([isbn, title, author])

        # Close the library file
        library_file.close()

        print "Saved", self.filename

if __name__ == "__main__":
    library = Library("library_test.csv")
    library.read_from_file()

    library.add_book(crwBook.Book("1234", "title1234", "author1234"))
    library.add_book(crwBook.Book("2345", "title2345", "author2345"))
    library.add_book(crwBook.Book("3456", "title3456", "author3456"))

    library.remove_isbn("2345")

    library.save_to_file()

    
