#!/usr/bin/env python

import crwBook

try:
    import urllib.request, urllib.error, urllib.parse
    from BeautifulSoup import BeautifulSoup, SoupStrainer
    HAVE_SOUP = True
except ImportError:
    print("### Sorry, I can't search for book info")
    HAVE_SOUP = False

class BaseSearcher(object):
    def search(self, isbn):
        book = crwBook.Book(str(isbn), "Title Unknown", "Author Unknown")
        return book
    
class UPCDatabaseCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.upcdatabase.com/item/"

    def search(self, isbn):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn)

class LibraryThingCom(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.librarything.com/tag/"

    def search(self, isbn):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn)

class ISBNSearchOrg(BaseSearcher):
    def __init__(self):
        self.search_url = "http://www.isbnsearch.org/isbn/"

        # Only process the bookinfo division
        self.bookinfo_filter = SoupStrainer("div", "bookinfo")

    def search(self, isbn):
        # Call the superclass method to create the book
        book = super(ISBNSearchOrg, self).search(isbn)

        if HAVE_SOUP == True:
            full_url = self.search_url + isbn
            try:
                page = urllib.request.urlopen(full_url)
                soup = BeautifulSoup(page.read(),
                    parseOnlyThese= self.bookinfo_filter)

                # get the original encoding
                original_encoding = soup.originalEncoding

                # Get the title, which may fail
                try:
                    # This will be in unicode
                    book.set_title(soup.h2.string)
                except AttributeError:
                    print("### Error retrieving Title.")
                    book.set_title("AttributeError")

                # Get the author
                for label in soup.findAll("strong"):
                    if label.string == "Author:":
                        try:
                            # This will be in unicode
                            book.set_author(label.nextSibling)
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.set_author("AttributeError")
                    if label.string == "Authors:":
                        try:
                            # This will be in unicode
                            book.set_author(label.nextSibling)
                        except AttributeError:
                            print("### Error retrieving Author.")
                            book.set_author("AttributeError")
                            
            except urllib.error.URLError:
                print("### Could not contact server.")
        return book

