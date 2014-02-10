#!/usr/bin/env python3

from html import entities
import collections

class BookDict(dict):
    def __init__(self, *args, **kwargs):
        super(BookDict, self).__init__(*args, **kwargs)
        self['found'] = False
        self['title'] = "Unknown Title"
        self['authors'] = "Unknown Author"
        
BookTuple = collections.namedtuple('BookTuple', ['found', 'isbn', 'title', 'authors'])

(bkISBN, bkTitle, bkAuthor, bkBinding, bkPublisher, bkPublished) = list(range(6))
bkFields = {
    bkISBN : "ISBN",
    bkTitle : "Title",
    bkAuthor : "Author",
    bkBinding : "Binding",
    bkPublisher : "Publisher",
    bkPublished : "Published"
}

def check_and_sanitise(s):
    # TODO: Parse the input string for non-escaped html entities
    pass

class Book(object):
    def __init__(self, isbn, title=None, author=None):
        self.binding = None
        self.publisher = None
        self.published = None
        try:
            # The ISBN
            self.isbn = isbn.strip()

            # The Title
            if title != None:
                self.title = title.strip()

            # The Author
            if author != None:
                self.author = author.strip()

        except AttributeError:
            print("### Could not set book fields.")

    def set_isbn(self, isbn):
        try:
            self.isbn = isbn.strip()
        except AttributeError:
            print("### Could not set ISBN")
            self.isbn = "Unknown ISBN"

    def get_isbn(self):
        return self.isbn

    def set_title(self, title):
        try:
            self.title = title.strip()
        except AttributeError:
            print("### Could not set title")
            self.title = "Unknown Title"

    def get_title(self):
        return self.title

    def set_author(self, author):
        try:
            self.author = author.strip()
        except AttributeError:
            print("### Could not set author")
            self.author = "Unknown Author"

    def get_author(self):
        return self.author

    def set_isbn_13(self, isbn13):
        self.isbn_13 = isbn13.strip()

    def get_isbn_13(self):
        return self.isbn_13

    def set_isbn_10(self, isbn10):
        self.isbn_10 = isbn10.strip()

    def get_isbn_10(self):
        return self.isbn_10

    def set_binding(self, binding):
        self.binding = binding.strip()

    def get_binding(self):
        return self.binding

    def set_publisher(self, publisher):
        self.publisher = publisher.strip()

    def get_publisher(self):
        return self.publisher

    def set_published(self, published):
        self.published = published.strip()

    def get_published(self):
        return self.published

    def __repr__(self):
        return 'crwBook.Book("' + self.isbn + \
               '", "' + self.title + \
               '", "' + self.author + \
               '")'

    def __str__(self):
        return "ISBN:" + self.isbn + \
               ", Title:" + self.title + \
               ", Author:" + self.author

if __name__ == "__main__":
    book = Book(" 0586039899 ", " The Fabulous Riverboat", "  Philip Jos\u00e9 Farmer")
    print(book)
