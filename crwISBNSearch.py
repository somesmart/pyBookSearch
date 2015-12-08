#!/usr/bin/env python3

import crwBook
import json
import sys
# from pprint import pprint

try:
    import urllib.request
    import urllib.error
    import urllib.parse
    HAVE_URLLIB = True
except ImportError:
    import urllib2
    HAVE_URLLIB = False

try:
    from bs4 import BeautifulSoup, SoupStrainer
    HAVE_SOUP = True
except ImportError:
    print("### Sorry, I can't search for book info")
    HAVE_SOUP = False


class BaseSearcher(object):
    def search(self, isbn, book=None):
        if book is None:
            book = crwBook.Book(str(isbn))
        else:
            book.isbn = isbn
        return book


class UPCDatabaseCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.upcdatabase.com/item/"

    def search(self, isbn, book=None):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn, book=book)
        return book


class LibraryThingCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.librarything.com/tag/"

    def search(self, isbn, book=None):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn, book=book)
        return book


class OpenISBNCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.openisbn.com/isbn/"


class ISBNDBCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://isbndb.com/api/v2/json/[your-api-key]/book/"


class OpenLibraryOrg(BaseSearcher):

    def __init__(self):
        # Documentation at https://openlibrary.org/dev/docs/api/books
        self.search_url = "https://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json&jscmd=data"

    def search(self, isbn, book=None):
        # Call the superclass method to create the book
        book = super(OpenLibraryOrg, self).search(isbn, book=book)

        # Create the URL
        full_url = self.search_url.format(isbn)

        # Guard against URL errors
        try:

            # Open the URL
            page = urllib.request.urlopen(full_url)

            # We expect JSON data
            book_info = json.loads(page.read().decode())

            # identifiers -> {isbn_10, isbn_13, openlibrary, etc}
            # authors -> list of {name, url}
            # publish_date -> string
            # publishers -> list of {name}
            # title -> string
            # subtitle -> string

            # If there are no keys, there is no data
            if len(book_info.keys()) > 0:

                for k1 in book_info.keys():

                    # print('OpenLibraryOrg key: {}'.format(k1))

                    # Get the title and subtitle, join them
                    book.title = book_info[k1].get('title', 'Unknown')
                    subtitle = book_info[k1].get('subtitle', '')
                    if subtitle != '':
                        book.title = '{} : {}'.format(book.title, subtitle)

                    # Concatenate all the authors
                    if 'authors' in book_info[k1]:
                        authors = ';'.join(
                            [a['name'] for a in book_info[k1]['authors']])
                        if authors != '':
                            book.author = authors

                    # Concatenate all the publishers
                    if 'publishers' in book_info[k1]:
                        publishers = ';'.join(
                            [p['name'] for p in book_info[k1]['publishers']])
                        if publishers != '':
                            book.publisher = publishers

                    # Get the published date
                    book.published = book_info[k1].get('publish_date', 'Unknown')

            else:
                print ("No openlibrary.org data")

        except urllib.error.URLError as err:
            print("URLError {}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return book


class ISBNSearchOrg(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.isbnsearch.org/isbn/"

        # Only process the core content division
        self.bookinfo_filter = SoupStrainer("div")

    def search(self, isbn, book=None):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn, book=book)

        if HAVE_SOUP:
            full_url = self.search_url + str(isbn)
            try:
                if HAVE_URLLIB:
                    urlexception = urllib.error.URLError
                    page = urllib.request.urlopen(full_url)
                else:
                    urlexception = urllib2.URLError
                    page = urllib2.urlopen(full_url)

                soup = BeautifulSoup(
                    page.read(),
                    "html.parser",
                    parse_only=self.bookinfo_filter)

                # get the original encoding
                # original_encoding = soup.originalEncoding
                # print ("encoding: ".format(original_encoding))

                # Get the title, which may fail
                try:
                    # TODO: This is a hack for &
                    # TODO: make html/xml safe
                    book.title = soup.h2.string.replace("&", "&amp;")
                    print ("title: {}".format(soup.h2.string))
                except AttributeError:
                    print("### Error retrieving Title.")
                    book.title = "Unknown"

                # Get the remaining values
                for label in soup.find_all('strong'):

                    # Get the author
                    if label.string == "Author:":
                        try:
                            # TODO: This is a hack for &
                            # TODO: make html/xml safe
                            book.author = label.nextSibling.string.replace(
                                "&", "&amp;")
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.author = "Unknown"

                    if label.string == "Authors:":
                        try:
                            # TODO: This is a hack for &
                            # TODO: make html/xml safe
                            book.author = label.nextSibling.replace(
                                "&", "&amp;")
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.author = "Unknown"

                    if label.string == "Binding:":
                        # TODO: This is a hack for &
                        book.binding = label.nextSibling.replace(
                            "&", "&amp;")

                    if label.string == "Publisher:":
                        # TODO: This is a hack for &
                        book.publisher = label.nextSibling.replace(
                            "&", "&amp;")

                    if label.string == "Published:":
                        # TODO: This is a hack for &
                        book.published = label.nextSibling.replace(
                            "&", "&amp;")

                # pull the sixth record from the price list (gets the first used price)
                try:
                    book.usedPrice = soup.find_all('p', class_='pricelink')[5].a.contents
                # if there isn't a sixth record just error out
                except IndexError:
                    book.usedPrice = "X"

            except urlexception as err:
                print("ISBN not found at www.isbnsearch.org: {}".format(err.code))

        return book

