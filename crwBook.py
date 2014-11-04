#!/usr/bin/env python3

from html import entities
import collections


# class BookDict(dict):
#     def __init__(self, *args, **kwargs):
#         super(BookDict, self).__init__(*args, **kwargs)
#         self['found'] = False
#         self['title'] = "Unknown Title"
#         self['authors'] = "Unknown Author"

# BookTuple = collections.namedtuple('BookTuple', ['found', 'isbn', 'title', 'authors'])

(
    bkISBN,
    bkTitle,
    bkAuthor,
    bkBinding,
    bkPublisher,
    bkPublished
) = list(range(6))

bkFields = {
    bkISBN: "ISBN",
    bkTitle: "Title",
    bkAuthor: "Author",
    bkBinding: "Binding",
    bkPublisher: "Publisher",
    bkPublished: "Published"
}


def check_and_sanitise(s):
    # TODO: Parse the input string for non-escaped html entities
    pass


class Book(object):
    def __init__(self, isbn, title='Unknown', author='Unknown'):
        self._binding = 'Unknown'
        self._publisher = 'Unknown'
        self._published = 'Unknown'

        try:
            # The ISBN
            self._isbn = isbn.strip()

            # The Title
            self._title = title.strip()

            # The Author
            self._author = author.strip()

        except AttributeError as err:
            print("Error setting book fields: {}".format(err))

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        self._isbn = value.strip()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        self._author = value.strip()

    @property
    def binding(self):
        return self._binding

    @binding.setter
    def binding(self, value):
        self._binding = value.strip()

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        self._publisher = value.strip()

    @property
    def published(self):
        return self._published

    @published.setter
    def published(self, value):
        self._published = value.strip()

    def __repr__(self):
        return 'crwBook.Book("' + self._isbn + \
               '", "' + self._title + \
               '", "' + self._author + \
               '")'

    def __str__(self):
        return "ISBN:" + self._isbn + \
               ", Title:" + self._title + \
               ", Author:" + self._author

if __name__ == "__main__":
    book = Book(" 0586039899 ", " The Fabulous Riverboat", "  Philip Jos\u00e9 Farmer")
    print(book)
