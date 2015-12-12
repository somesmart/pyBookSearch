#!/usr/bin/env python3

from html import entities
import collections


# The order of fields in bkFields
(
    bkISBN,
    bkISBN10,
    bkISBN13,
    bkLCCN,
    bkTitle,
    bkAuthor,
    bkBinding,
    bkPublisher,
    bkPublished,
    bkUsedPrice
) = list(range(10))

# A mapping from Book properties to CSV Column Titles.
bkFields = [
    ('isbn', "ISBN"),
    ('isbn10', "ISBN10"),
    ('isbn13', "ISBN13"),
    ('lccn', "LCCN"),
    ('title', "Title"),
    ('author', "Author"),
    ('binding', "Binding"),
    ('publisher', "Publisher"),
    ('published', "Published"),
    ('usedPrice', "UsedPrice")
]

UNKNOWN = 'Unknown'


def check_and_sanitise(s):
    # TODO: Parse the input string for non-escaped html entities
    pass


class Book(object):
    '''
    A class to hold book information.
    '''

    def __init__(self, **kwargs):
        '''
        Initialise the book from the given keyword arguments
        by iterating through bkFields and looking through kwargs
        for either the property name (f[0]) or the column name (f[1]),
        with a preference for the property name. If neither are found,
        UNKNOWN is used as the default.
        '''

        for f in bkFields:
            setattr(
                self,
                f[0],
                kwargs.get(
                    f[0],
                    kwargs.get(
                        f[1],
                        UNKNOWN)))

    def update_unknowns(self, **kwargs):
        '''
        Update the book information from the given keyword arguments,
        but only if the current book information is UNKNOWN.
        '''

        for f in bkFields:
            if getattr(self, f[0]) == UNKNOWN:
                setattr(
                    self,
                    f[0],
                    kwargs.get(
                        f[0],
                        kwargs.get(
                            f[1],
                            UNKNOWN)))

    def display_unknowns(self, **kwargs):
        '''
        Display the unknown fields in a book
        '''

        for f in bkFields:
            if getattr(self, f[0]) == UNKNOWN:
                print(f[0])

    @property
    def has_unknowns(self):
        for f in bkFields:
            if getattr(self, f[0]) == UNKNOWN:
                return True
        return False

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, value):
        if value is not None:
            self._isbn = value.strip()

    @property
    def isbn10(self):
        return self._isbn10

    @isbn10.setter
    def isbn10(self, value):
        if value is not None:
            self._isbn10 = value.strip()

    @property
    def isbn13(self):
        return self._isbn13

    @isbn13.setter
    def isbn13(self, value):
        if value is not None:
            self._isbn13 = value.strip()

    @property
    def lccn(self):
        return self._lccn

    @lccn.setter
    def lccn(self, value):
        if value is not None:
            self._lccn = value.strip()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value is not None:
            self._title = value.strip()

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if value is not None:
            self._author = value.strip()

    @property
    def binding(self):
        return self._binding

    @binding.setter
    def binding(self, value):
        if value is not None:
            self._binding = value.strip()

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, value):
        if value is not None:
            self._publisher = value.strip()

    @property
    def published(self):
        return self._published

    @published.setter
    def published(self, value):
        if value is not None:
            self._published = value.strip()

    @property
    def usedPrice(self):
        return self._usedPrice

    @usedPrice.setter
    def usedPrice(self, value):
        if value is not None:
            self._usedPrice = value

    def __repr__(self):
        return 'crwBook.Book(isbn="' + self._isbn + \
               '", title="' + self._title + \
               '", author="' + self._author + \
               '")'

    def __str__(self):
        return "ISBN:" + self._isbn + \
               ", Title:" + self._title + \
               ", Author:" + self._author

if __name__ == "__main__":
    book = Book(
        isbn=" 0586039899 ",
        title=" The Fabulous Riverboat",
        author="  Philip Jos\u00e9 Farmer")
    print(book)
