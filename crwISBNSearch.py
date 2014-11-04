#!/usr/bin/env python3

import crwBook
import json
import sys

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
        # TODO: Not the actual URL
        #self.search_url = "https://openlibrary.org/dev/docs/api/books"
        #self.search_url = "https://openlibrary.org/api/books?bibkeys=ISBN:0451526538&callback=mycallback"
        self.search_url = "https://openlibrary.org/api/books?bibkeys=ISBN:{}&format=json&jscmd=data"

    def search(self, isbn, book=None):
        # Call the superclass method to create the book
        #book = super(OpenLibraryOrg, self).search(isbn, book=book)
        book = {"found": False, "isbn": isbn, "title": "Unknown", "authors": "Unknown"}

        # Create the URL
        full_url = self.search_url.format(isbn)

        # Guard against URL errors
        try:

            # Open the URL
            page = urllib.request.urlopen(full_url)

            # We expect JSON data
            book_info = json.loads(page.read().decode())

            # If there are no keys, there is no data
            if len(book_info.keys()) > 0:
                for k1 in book_info.keys():
                    try:
                        title = book_info[k1]['title']
                        book["title"] = title
                        book["found"] = True
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

                    try:
                        authors = ""
                        for a1 in book_info[k1]['authors']:
                            authors += "{};".format(a1['name'])
                        if authors != "":
                            book["authors"] = authors[:-1]
                            book["found"] = True
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        raise

            else:
                print ("No data")

        except urllib.error.URLError as err:
            print("URLError {}".format(err))
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

        return book


class ISBNSearchOrg(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.isbnsearch.org/isbn/"

        # Only process the bookinfo division
        self.bookinfo_filter = SoupStrainer("div", "bookinfo")

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

                soup = BeautifulSoup(page.read(),
                    parse_only = self.bookinfo_filter)

                # get the original encoding
                original_encoding = soup.originalEncoding
                print ("encoding: ".format(original_encoding))

                # Get the title, which may fail
                try:
                    # TODO: This is a hack for &
                    # TODO: make html/xml safe
                    book.title = soup.h2.string.replace("&", "&amp;")
                    print ("title: {}".format(soup.h2.string))
                except AttributeError:
                    print("### Error retrieving Title.")
                    book.title = "Unknown"

                # Get the author
                for label in soup.findAll("strong"):

                    if label.string == "Author:":
                        try:
                            # TODO: This is a hack for &
                            # TODO: make html/xml safe
                            book.author = label.nextSibling.replace("&", "&amp;")
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.author = "Unknown"

                    if label.string == "Authors:":
                        try:
                            # TODO: This is a hack for &
                            # TODO: make html/xml safe
                            book.author = label.nextSibling.replace("&", "&amp;")
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.author = "Unknown"

                    if label.string == "Binding:":
                        # TODO: This is a hack for &
                        book.binding = label.nextSibling.replace("&", "&amp;")

                    if label.string == "Publisher:":
                        # TODO: This is a hack for &
                        book.publisher = label.nextSibling.replace("&", "&amp;")

                    if label.string == "Published:":
                        # TODO: This is a hack for &
                        book.published = label.nextSibling.replace("&", "&amp;")

            except urlexception:
                print("### Could not contact server.")
        return book

