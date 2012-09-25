#!/usr/bin/env python

STR_ISBN = "ISBN"
STR_TITLE = "Title"
STR_AUTHOR = "Author"

class Book(object):
    def __init__(self, isbn, title=None, author=None):
        ''' Converts all inputs to unicode, and stores them.
        '''
        try:
            # The ISBN
            if type(isbn) == str:
                isbn = unicode(isbn)
            self.u_isbn = isbn.strip()

            # The Title
            if title != None:
                if type(title) == str:
                    title = unicode(title)
                self.u_title = title.strip()

            # The Author
            if author != None:
                if type(author) == str:
                    author = unicode(author)
                self.u_author = author.strip()

        except AttributeError:
            print "### Could not set book fields."

    def set_isbn(self, isbn):
        try:
            if type(isbn) == str:
                isbn = unicode(isbn)
            self.u_isbn = isbn.strip()
        except AttributeError:
            print "### Could not set ISBN"
            self.u_isbn = u"AttributeError"

    def get_isbn(self):
        return self.u_isbn

    def set_title(self, title):
        try:
            if type(title) == str:
                title = unicode(title)
            self.u_title = title.strip()
        except AttributeError:
            print "### Could not set title"
            self.u_title = u"AttributeError"

    def get_title(self):
        return self.u_title

    def set_author(self, author):
        try:
            if type(author) == str:
                author = unicode(author)
            self.u_author = author.strip()
        except AttributeError:
            print "### Could not set author"
            self.u_author = u"AttributeError"

    def get_author(self):
        return self.u_author

    def __repr__(self):
        return 'crwBook.Book("' + self.u_isbn + \
               '", "' + self.u_title + \
               '", "' + self.u_author + \
               '")'

    def __str__(self):
        return "ISBN:" + self.u_isbn.encode("iso-8859-1") + \
               ", Title:" + self.u_title.encode("iso-8859-1") + \
               ", Author:" + self.u_author.encode("iso-8859-1")

if __name__ == "__main__":
    book = Book(u" 0586039899 ", u" The Fabulous Riverboat", u"  Philip Jos\u00e9 Farmer")
    print book
